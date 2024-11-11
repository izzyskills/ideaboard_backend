from datetime import datetime
from typing import Dict, List, Optional, Tuple
import uuid
from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import array_agg
from sqlmodel import and_, desc, func, or_, select, case, distinct
from sqlmodel.sql.expression import Select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import (
    Idea,
    Comment,
    IdeaCategoryAssociation,
    Project,
    Vote,
    Category,
    User,
)
from src.errors import (
    CategoryNotFound,
    IdeaNotFound,
    ProjectNotFound,
    UserNotFound,
    VoteNotFound,
)
from src.ideas.schemas import (
    CommentCreationModel,
    IdeaCreationModel,
    IdeaSearchParams,
    VoteCreationModel,
)


class IdeaService:
    async def create_idea(self, idea_data: IdeaCreationModel, session: AsyncSession):
        idea_data_dict = idea_data.model_dump()

        # get user it
        created_by_id = idea_data_dict["creator_id"]
        user = await session.exec(select(User).where(User.id == created_by_id))
        user = user.first()
        if user is None:
            raise UserNotFound

        # Validate categories
        category_ids = idea_data_dict["category_id"]
        categories = await session.exec(
            select(Category).where(Category.id == category_ids)
        )
        categories = categories.all()
        if categories is None:
            raise CategoryNotFound
        print(categories)

        # Validate project
        project_id = idea_data_dict["project_id"]
        project = await session.exec(select(Project).where(Project.id == project_id))
        project = project.one_or_none()
        if project is None:
            raise ProjectNotFound

        # Create new idea
        new_idea = Idea(
            **{
                "title": idea_data_dict["title"],
                "description": idea_data_dict["description"],
                "creator_id": idea_data_dict["creator_id"],
                "project_id": idea_data_dict["project_id"],
                "categories": categories,
            }
        )
        session.add(new_idea)
        await session.commit()
        await session.refresh(new_idea)

        return new_idea

    async def search_ideas(
        self,
        session: AsyncSession,
        params: IdeaSearchParams,
        current_user_id: Optional[uuid.UUID] = None,
    ) -> Tuple[List[Dict], Optional[datetime]]:
        try:
            upvotes_subquery = (
                select(Vote.idea_id, func.count(Vote.id).label("upvotes"))
                .where(Vote.is_upvote.is_(True))
                .group_by(Vote.idea_id)
                .subquery()
            )

            downvotes_subquery = (
                select(Vote.idea_id, func.count(Vote.id).label("downvotes"))
                .where(Vote.is_upvote.is_(False))
                .group_by(Vote.idea_id)
                .subquery()
            )
            # First, get the ideas with votes and basic info
            main_query = (
                select(
                    Idea,
                    Project.name.label("project_name"),
                    User.username.label("creator_username"),
                    func.coalesce(upvotes_subquery.c.upvotes, 0).label("upvotes"),
                    func.coalesce(downvotes_subquery.c.downvotes, 0).label("downvotes"),
                    func.bool_or(
                        and_(Vote.user_id == current_user_id, Vote.is_upvote.is_(True))
                    ).label("user_upvoted"),
                    func.bool_or(
                        and_(Vote.user_id == current_user_id, Vote.is_upvote.is_(False))
                    ).label("user_downvoted"),
                    func.count(case((Comment.user_id == current_user_id, 1))).label(
                        "user_commented"
                    ),
                    array_agg(distinct(Category.name)).label("category_names"),
                )
                .join(Project, Idea.project_id == Project.id)
                .join(User, Idea.creator_id == User.id)
                .outerjoin(Vote, Vote.idea_id == Idea.id)
                .outerjoin(Comment, Comment.idea_id == Idea.id)
                .outerjoin(
                    IdeaCategoryAssociation, IdeaCategoryAssociation.idea_id == Idea.id
                )
                .outerjoin(Category, Category.id == IdeaCategoryAssociation.category_id)
                .outerjoin(upvotes_subquery, upvotes_subquery.c.idea_id == Idea.id)
                .outerjoin(downvotes_subquery, downvotes_subquery.c.idea_id == Idea.id)
                .group_by(
                    Idea.id,
                    Project.id,
                    User.id,
                    upvotes_subquery.c.upvotes,
                    downvotes_subquery.c.downvotes,
                )
            )

            # # Apply filters
            # if params.category_ids:
            #     main_query = main_query.join(IdeaCategory).where(
            #         IdeaCategory.category_id.in_(params.category_ids)
            #     )
            #
            if params.project_id:
                main_query = main_query.where(Idea.project_id == params.project_id)

            if params.text:
                search_pattern = f"%{params.text}%"
                main_query = main_query.where(
                    or_(
                        Idea.title.ilike(search_pattern),
                        Idea.description.ilike(search_pattern),
                        Project.name.ilike(search_pattern),
                        User.username.ilike(search_pattern),
                        Category.name.ilike(search_pattern),
                    )
                )

            if params.cursor:
                main_query = main_query.where(Idea.created_at < params.cursor)

            # Add grouping and ordering
            main_query = (
                main_query.group_by(
                    Idea.id,
                    Project.name,
                    User.username,
                )
                .order_by(Idea.created_at.desc())
                .limit(params.limit)
            )

            # Execute main query
            results = await session.execute(main_query)
            rows = results.all()

            # Get all idea IDs from the results
            idea_ids = [row.Idea.id for row in rows]

            # Fetch latest comments for all ideas in a single query
            comments_query = (
                select(
                    Comment.idea_id,
                    Comment.content,
                    Comment.created_at,
                    User.username.label("commenter_username"),
                )
                .join(User, User.id == Comment.user_id)
                .where(Comment.idea_id.in_(idea_ids))
                .order_by(Comment.idea_id, Comment.created_at.desc())
            )

            comments_results = await session.execute(comments_query)
            comments_rows = comments_results.all()

            # Group comments by idea_id
            comment_count = {}
            comments_by_idea = {}
            for comment in comments_rows:
                if comment.idea_id not in comments_by_idea:
                    comments_by_idea[comment.idea_id] = []
                if comment.idea_id not in comment_count:
                    comment_count[comment.idea_id] = 0
                comment_count[comment.idea_id] += 1
                if (
                    len(comments_by_idea[comment.idea_id]) < 2
                ):  # Only keep latest 2 comments
                    comments_by_idea[comment.idea_id].append(
                        {
                            "content": comment.content,
                            "created_at": comment.created_at.isoformat(),
                            "commenter_username": comment.commenter_username,
                        }
                    )

            # Process results
            ideas_list = []
            for row in rows:
                idea_dict = {
                    "id": str(row.Idea.id),
                    "title": row.Idea.title,
                    "description": row.Idea.description,
                    "project_id": str(row.Idea.project_id),
                    "project_name": row.project_name,
                    "creator_id": str(row.Idea.creator_id),
                    "creator_username": row.creator_username,
                    "created_at": row.Idea.created_at.isoformat(),
                    "category_names": row.category_names,
                    "votes": {
                        "upvotes": row.upvotes,
                        "downvotes": row.downvotes,
                        "total": row.upvotes + row.downvotes,
                        "score": row.upvotes - row.downvotes,
                    },
                    "comments": comments_by_idea.get(row.Idea.id, []),
                    "comments_count": comment_count.get(row.Idea.id, 0),
                }

                # Add user-specific data if user_id provided
                if current_user_id:
                    idea_dict["user_vote"] = {
                        "has_voted": bool(row.user_upvoted or row.user_downvoted),
                        "is_upvote": (
                            bool(row.user_upvoted)
                            if (row.user_upvoted or row.user_downvoted)
                            else None
                        ),
                    }
                    idea_dict["has_commented"] = bool(row.user_commented)

                ideas_list.append(idea_dict)

            # Calculate next cursor
            next_cursor = (
                rows[-1].Idea.created_at if len(rows) == params.limit else None
            )

            return ideas_list, next_cursor
        except Exception as e:
            print(f"Error in search_ideas: {str(e)}")
            raise HTTPException(
                status_code=500, detail="An error occurred while searching ideas"
            )

    async def get_idea_by_id(
        self,
        idea_id: uuid.UUID,
        session: AsyncSession,
        current_user_id: Optional[uuid.UUID] = None,
    ):
        try:
            # Subqueries for upvotes and downvotes
            upvotes_subquery = (
                select(Vote.idea_id, func.count(Vote.id).label("upvotes"))
                .where(Vote.is_upvote.is_(True))
                .group_by(Vote.idea_id)
                .subquery()
            )

            downvotes_subquery = (
                select(Vote.idea_id, func.count(Vote.id).label("downvotes"))
                .where(Vote.is_upvote.is_(False))
                .group_by(Vote.idea_id)
                .subquery()
            )

            # Main query for idea details and votes
            main_query = (
                select(
                    Idea,
                    Project.name.label("project_name"),
                    User.username.label("creator_username"),
                    func.coalesce(upvotes_subquery.c.upvotes, 0).label("upvotes"),
                    func.coalesce(downvotes_subquery.c.downvotes, 0).label("downvotes"),
                    func.bool_or(
                        and_(Vote.user_id == current_user_id, Vote.is_upvote.is_(True))
                    ).label("user_upvoted"),
                    func.bool_or(
                        and_(Vote.user_id == current_user_id, Vote.is_upvote.is_(False))
                    ).label("user_downvoted"),
                    func.count(case((Comment.user_id == current_user_id, 1))).label(
                        "user_commented"
                    ),
                    array_agg(distinct(Category.name)).label("category_names"),
                )
                .join(Project, Idea.project_id == Project.id)
                .join(User, Idea.creator_id == User.id)
                .outerjoin(Vote, Vote.idea_id == Idea.id)
                .outerjoin(Comment, Comment.idea_id == Idea.id)
                .outerjoin(
                    IdeaCategoryAssociation, IdeaCategoryAssociation.idea_id == Idea.id
                )
                .outerjoin(Category, Category.id == IdeaCategoryAssociation.category_id)
                .outerjoin(upvotes_subquery, upvotes_subquery.c.idea_id == Idea.id)
                .outerjoin(downvotes_subquery, downvotes_subquery.c.idea_id == Idea.id)
                .where(Idea.id == idea_id)
                .group_by(
                    Idea.id,
                    Project.id,
                    User.id,
                    upvotes_subquery.c.upvotes,
                    downvotes_subquery.c.downvotes,
                )
            )

            # Execute main query
            results = await session.execute(main_query)
            row = results.one_or_none()

            if not row:
                return None

            idea = row.Idea

            # Fetch all comments for the idea
            comments_query = (
                select(
                    Comment.id,
                    Comment.content,
                    Comment.created_at,
                    User.username.label("commenter_username"),
                    User.id.label("commenter_id"),
                )
                .join(User, User.id == Comment.user_id)
                .where(Comment.idea_id == idea_id)
                .order_by(Comment.created_at.desc())
            )

            comments_results = await session.execute(comments_query)
            comments = comments_results.all()

            # Build the response dictionary
            idea_dict = {
                "id": str(idea.id),
                "title": idea.title,
                "description": idea.description,
                "project_id": str(idea.project_id),
                "project_name": row.project_name,
                "creator_id": str(idea.creator_id),
                "creator_username": row.creator_username,
                "created_at": idea.created_at.isoformat(),
                "category_names": row.category_names,
                "votes": {
                    "upvotes": row.upvotes,
                    "downvotes": row.downvotes,
                    "total": row.upvotes + row.downvotes,
                    "score": row.upvotes - row.downvotes,
                },
                "comments": [
                    {
                        "id": str(comment.id),
                        "content": comment.content,
                        "created_at": comment.created_at.isoformat(),
                        "commenter_username": comment.commenter_username,
                        "commenter_id": str(comment.commenter_id),
                        "is_user_comment": (
                            str(comment.commenter_id) == str(current_user_id)
                            if current_user_id
                            else False
                        ),
                    }
                    for comment in comments
                ],
                "comments_count": len(comments),
            }

            # Add user-specific data if user_id was provided
            if current_user_id:
                idea_dict["has_commented"] = bool(row.user_commented)
                idea_dict["user_vote"] = {
                    "has_voted": bool(row.user_upvoted or row.user_downvoted),
                    "is_upvote": (
                        bool(row.user_upvoted)
                        if (row.user_upvoted or row.user_downvoted)
                        else None
                    ),
                }

            return idea_dict

        except Exception as e:
            print(f"Error in get_idea_by_id: {str(e)}")
            raise HTTPException(
                status_code=500, detail="An error occurred while fetching the idea"
            )

    async def create_comment(
        self, comment_data: CommentCreationModel, session: AsyncSession
    ):
        comment_data_dict = comment_data.model_dump()
        user = await session.exec(
            select(User).where(User.id == comment_data_dict["user_id"])
        )
        user = user.first()
        if user is None:
            raise UserNotFound
        idea = await session.exec(
            select(Idea).where(Idea.id == comment_data_dict["idea_id"])
        )
        idea = idea.first()
        if idea is None:
            raise IdeaNotFound
        comment = Comment(**comment_data_dict)
        session.add(comment)
        await session.commit()
        await session.refresh(comment)
        return comment

    async def get_vote_counts(
        self,
        idea_id: uuid.UUID,
        session: AsyncSession,
        current_user_id: uuid.UUID | None = None,
    ):
        print("hello vote counts")
        query = select(
            func.count(case((Vote.is_upvote.is_(True), 1))).label("upvotes"),
            func.count(case((Vote.is_upvote.is_(False), 1))).label("downvotes"),
            func.count(
                case(
                    (
                        and_(
                            Vote.user_id == current_user_id,
                            Vote.is_upvote.is_(True),
                        ),
                        1,
                    )
                )
            ).label("user_upvoted"),
            func.count(
                case(
                    (
                        and_(
                            Vote.user_id == current_user_id,
                            Vote.is_upvote.is_(False),
                        ),
                        1,
                    )
                )
            ).label("user_downvoted"),
        ).where(Vote.idea_id == idea_id)

        result = await session.execute(query)
        row = result.one()
        # Assuming `row` is an object with the required attributes
        print(f"Upvotes: {row.upvotes}")
        print(f"Downvotes: {row.downvotes}")
        print(f"User Upvoted: {row.user_upvoted}")
        print(f"User Downvoted: {row.user_downvoted}")

        print(row)
        dict = {
            "upvotes": row.upvotes,
            "downvotes": row.downvotes,
            "total": row.upvotes + row.downvotes,
            "score": row.upvotes - row.downvotes,
            "has_voted": bool(row.user_upvoted or row.user_downvoted),
            "is_upvote": (
                bool(row.user_upvoted)
                if (row.user_upvoted or row.user_downvoted)
                else None
            ),
        }
        print(dict)
        return dict

    async def handle_vote(
        self,
        idea_id: uuid.UUID,
        user_id: uuid.UUID,
        vote_data: VoteCreationModel,
        session: AsyncSession,
    ) -> Vote | None:
        # Check for existing vote
        result = await session.exec(
            select(Vote).where(and_(Vote.idea_id == idea_id, Vote.user_id == user_id))
        )
        existing_vote = result.one_or_none()

        if existing_vote:
            # Update existing vote if different
            if existing_vote.is_upvote != vote_data.is_upvote:
                existing_vote.is_upvote = vote_data.is_upvote
                await session.commit()
                return existing_vote
            else:
                await session.delete(existing_vote)
                await session.commit()
                return None
        else:
            # Create new vote
            new_vote = Vote(
                **{
                    "user_id": user_id,
                    "idea_id": idea_id,
                    "is_upvote": vote_data.is_upvote,
                }
            )
            session.add(new_vote)
            await session.commit()
            return new_vote

    async def delete_vote(
        self, idea_id: uuid.UUID, user_id: uuid.UUID, session: AsyncSession
    ):
        result = await session.exec(
            select(Vote).where(and_(Vote.idea_id == idea_id, Vote.user_id == user_id))
        )
        vote = result.one_or_none()

        if vote:
            await session.delete(vote)
            await session.commit()
            return vote

        raise VoteNotFound
