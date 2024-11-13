# **Ideaboard**

# **Ideaboard**

### **Info**

- **Description**:
  A REST API for a opensource idea sharing web service.

This REST API is able to;

- Create Read Update And delete ideas
- Add vote and downvote to ideas
- Add categories to ideas e.t.c.
- **TermsOfService**: https://example.com/tos
- **Version**: v1
- **Contact**
  - Name: Omola Israel
  - Url: https://github.com/izzyskills
- **License**
  - Name: MIT License
  - Url: https://opensource.org/license/mit

---

### **Paths**

### /api/v1/auth/register

**POST**

**Summary**: Register User

**Description**: Create user account using email, username, first_name, last_name
params:
user_data: UserCreateModel

**[ Request Body ]** \*

- application/json:

  - $schema: UserCreateModel

**Example Value**:

```json
{
    "username" : string,
    "email" : string,
    "password" : string
}
```

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

### /api/v1/auth/login

**POST**

**Summary**: Login Users

**[ Request Body ]** \*

- application/json:

  - $schema: UserLoginModel

**Example Value**:

```json
{
    "email" : string,
    "password" : string
}
```

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

### /api/v1/auth/refresh_token

**GET**

**Summary**: Get New Access Token

**[ Parameters ]**

| name          |   in   | description |  type  | required |
| :------------ | :----: | :---------- | :----: | :------: |
| refresh_token | cookie |             | string |          |

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

### /api/v1/auth/logout

**GET**

**Summary**: Revoke Token

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

### /api/v1/auth/password-reset-request

**POST**

**Summary**: Password Reset Request

**[ Request Body ]** \*

- application/json:

  - $schema: PasswordResetRequestModel

**Example Value**:

```json
{
    "email" : string
}
```

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

### /api/v1/auth/password-reset-confirm/{token}

**POST**

**Summary**: Reset Account Password

**[ Parameters ]**

| name  |  in  | description |  type  | required |
| :---- | :--: | :---------- | :----: | :------: |
| token | path |             | string |    \*    |

**[ Request Body ]** \*

- application/json:

  - $schema: PasswordResetConfirmModel

**Example Value**:

```json
{
    "new_password" : string,
    "confirm_new_password" : string
}
```

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

### /api/v1/auth/test-refresh-token

**GET**

**Summary**: Test Refresh Token

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

### /api/v1/project/

**GET**

**Summary**: Get All Projects

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

  - type: array ( $schema: Project )

**Example Value**:

```json
[
    {
        "id" : string,
        "name" : string,
        "description" : string,
        "url" : string,
        "creator_id" : string,
        "creted_at" : string
    }
]
```

**POST**

**Summary**: Create Project

**[ Request Body ]** \*

- application/json:

  - $schema: ProjectCreationModel

**Example Value**:

```json
{
    "name" : string,
    "description" : string,
    "url" : string,
    "creator_id" : string
}
```

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

  - $schema: Project

**Example Value**:

```json
{
    "id" : string,
    "name" : string,
    "description" : string,
    "url" : string,
    "creator_id" : string,
    "creted_at" : string
}
```

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

### /api/v1/project/{project_id}

**GET**

**Summary**: Get Project By Id

**[ Parameters ]**

| name       |  in  | description |  type  | required |
| :--------- | :--: | :---------- | :----: | :------: |
| project_id | path |             | string |    \*    |

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

  - $schema: Project

**Example Value**:

```json
{
    "id" : string,
    "name" : string,
    "description" : string,
    "url" : string,
    "creator_id" : string,
    "creted_at" : string
}
```

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

**PUT**

**Summary**: Update Project

**[ Parameters ]**

| name       |  in  | description |  type  | required |
| :--------- | :--: | :---------- | :----: | :------: |
| project_id | path |             | string |    \*    |

**[ Request Body ]** \*

- application/json:

  - $schema: ProjectUpdateModel

**Example Value**:

```json
{
    "name" : ,
    "description" : ,
    "url" :
}
```

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

  - $schema: Project

**Example Value**:

```json
{
    "id" : string,
    "name" : string,
    "description" : string,
    "url" : string,
    "creator_id" : string,
    "creted_at" : string
}
```

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

**DELETE**

**Summary**: Delete Project

**[ Parameters ]**

| name       |  in   | description |  type  | required |
| :--------- | :---: | :---------- | :----: | :------: |
| project_id | path  |             | string |    \*    |
| auto_error | query |             |        |          |

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

  - $schema: Project

**Example Value**:

```json
{
    "id" : string,
    "name" : string,
    "description" : string,
    "url" : string,
    "creator_id" : string,
    "creted_at" : string
}
```

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

### /api/v1/ideas/

**POST**

**Summary**: Create Idea

**[ Request Body ]** \*

- application/json:

  - $schema: IdeaCreationModel

**Example Value**:

```json
{
    "title" : string,
    "description" : string,
    "category_id" : integer,
    "creator_id" : string,
    "project_id" : string
}
```

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

**GET**

**Summary**: Search Ideas Route

**[ Parameters ]**

| name       |  in   | description | type | required |
| :--------- | :---: | :---------- | :--: | :------: |
| project_id | query |             |      |          |
| text       | query |             |      |          |
| limit      | query |             |      |          |
| cursor     | query |             |      |          |

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

### /api/v1/ideas/{idea_id}

**GET**

**Summary**: Get Idea By Id

**[ Parameters ]**

| name    |  in  | description |  type  | required |
| :------ | :--: | :---------- | :----: | :------: |
| idea_id | path |             | string |    \*    |

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

### /api/v1/ideas/{idea_id}/comment

**POST**

**Summary**: Make Comment

**[ Parameters ]**

| name    |  in  | description |  type  | required |
| :------ | :--: | :---------- | :----: | :------: |
| idea_id | path |             | string |    \*    |

**[ Request Body ]** \*

- application/json:

  - $schema: CommentCreationModel

**Example Value**:

```json
{
    "content" : string,
    "user_id" : string,
    "idea_id" : string
}
```

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

### /api/v1/ideas/{idea_id}/votes

**POST**

**Summary**: Vote

**[ Parameters ]**

| name    |  in  | description |  type  | required |
| :------ | :--: | :---------- | :----: | :------: |
| idea_id | path |             | string |    \*    |

**[ Request Body ]** \*

- application/json:

  - $schema: VoteCreationModel

**Example Value**:

```json
{
    "is_upvote" : boolean
}
```

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

**GET**

**Summary**: Get Votes

**[ Parameters ]**

| name    |  in  | description |  type  | required |
| :------ | :--: | :---------- | :----: | :------: |
| idea_id | path |             | string |    \*    |

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

**DELETE**

**Summary**: Remove Vote

**[ Parameters ]**

| name    |  in  | description |  type  | required |
| :------ | :--: | :---------- | :----: | :------: |
| idea_id | path |             | string |    \*    |

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

---

### **Components**

### Schemas

**CommentCreationModel**

**content**:

- **string**

  - _required: true_

  - _nullable: false_

**user_id**:

- **string**

  - _format: uuid_

  - _required: true_

  - _nullable: false_

**idea_id**:

- **string**

  - _format: uuid_

  - _required: true_

  - _nullable: false_

**HTTPValidationError**

**detail**:

- **array [ ValidationError ]**

  - _required: false_

  - _nullable: false_

**IdeaCreationModel**

**title**:

- **string**

  - _required: true_

  - _nullable: false_

**description**:

- **string**

  - _required: true_

  - _nullable: false_

**category_id**:

- **integer**

  - _required: true_

  - _nullable: false_

**creator_id**:

- **string**

  - _format: uuid_

  - _required: true_

  - _nullable: false_

**project_id**:

- **string**

  - _format: uuid_

  - _required: true_

  - _nullable: false_

**PasswordResetConfirmModel**

**new_password**:

- **string**

  - _required: true_

  - _nullable: false_

**confirm_new_password**:

- **string**

  - _required: true_

  - _nullable: false_

**PasswordResetRequestModel**

**email**:

- **string**

  - _required: true_

  - _nullable: false_

**Project**

**id**:

- **string**

  - _format: uuid_

  - _required: true_

  - _nullable: false_

**name**:

- **string**

  - _required: true_

  - _nullable: false_

**description**:

- **string**

  - _required: true_

  - _nullable: false_

**url**:

- **string**

  - _required: true_

  - _nullable: false_

**creator_id**:

- **string**

  - _format: uuid_

  - _required: true_

  - _nullable: false_

**creted_at**:

- **string**

  - _format: date-time_

  - _required: true_

  - _nullable: false_

**ProjectCreationModel**

**name**:

- **string**

  - _required: true_

  - _nullable: false_

**description**:

- **string**

  - _required: true_

  - _nullable: false_

**url**:

- **string**

  - _required: true_

  - _nullable: false_

**creator_id**:

- **string**

  - _format: uuid_

  - _required: true_

  - _nullable: false_

**ProjectUpdateModel**

**name**:

    - _required: false_

    - _nullable: false_

**description**:

    - _required: false_

    - _nullable: false_

**url**:

    - _required: false_

    - _nullable: false_

**UserCreateModel**

**username**:

- **string**

  - _required: true_

  - _nullable: false_

  - _maxLength: 25_

**email**:

- **string**

  - _required: true_

  - _nullable: false_

  - _maxLength: 40_

**password**:

- **string**

  - _required: true_

  - _nullable: false_

  - _minLength: 6_

**UserLoginModel**

**email**:

- **string**

  - _required: true_

  - _nullable: false_

  - _maxLength: 40_

**password**:

- **string**

  - _required: true_

  - _nullable: false_

  - _minLength: 6_

**ValidationError**

**loc**:

    - _required: true_

    - _nullable: false_

**msg**:

- **string**

  - _required: true_

  - _nullable: false_

**type**:

- **string**

  - _required: true_

  - _nullable: false_

**VoteCreationModel**

**is_upvote**:

- **boolean**

  - _required: true_

  - _nullable: false_

---

### Security Schemes

**AccessTokenBearer**

- type: http

- scheme: bearer

**OptionalAccessTokenBearer**

- type: http

- scheme: bearer

---

### **Info**

- **Description**:
  A REST API for a opensource idea sharing web service.

This REST API is able to;

- Create Read Update And delete ideas
- Add vote and downvote to ideas
- Add categories to ideas e.t.c.
- **TermsOfService**: https://example.com/tos
- **Version**: v1
- **Contact**
  - Name: Omola Israel
  - Url: https://github.com/izzyskills
- **License**
  - Name: MIT License
  - Url: https://opensource.org/license/mit

---

### **Paths**

### /api/v1/auth/register

**POST**

**Summary**: Register User

**Description**: Create user account using email, username, first_name, last_name
params:
user_data: UserCreateModel

**[ Request Body ]** \*

- application/json:

  - $schema: UserCreateModel

**Example Value**:

```json
{
    "username" : string,
    "email" : string,
    "password" : string
}
```

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

### /api/v1/auth/login

**POST**

**Summary**: Login Users

**[ Request Body ]** \*

- application/json:

  - $schema: UserLoginModel

**Example Value**:

```json
{
    "email" : string,
    "password" : string
}
```

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

### /api/v1/auth/refresh_token

**GET**

**Summary**: Get New Access Token

**[ Parameters ]**

| name          |   in   | description |  type  | required |
| :------------ | :----: | :---------- | :----: | :------: |
| refresh_token | cookie |             | string |          |

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

### /api/v1/auth/logout

**GET**

**Summary**: Revoke Token

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

### /api/v1/auth/password-reset-request

**POST**

**Summary**: Password Reset Request

**[ Request Body ]** \*

- application/json:

  - $schema: PasswordResetRequestModel

**Example Value**:

```json
{
    "email" : string
}
```

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

### /api/v1/auth/password-reset-confirm/{token}

**POST**

**Summary**: Reset Account Password

**[ Parameters ]**

| name  |  in  | description |  type  | required |
| :---- | :--: | :---------- | :----: | :------: |
| token | path |             | string |    \*    |

**[ Request Body ]** \*

- application/json:

  - $schema: PasswordResetConfirmModel

**Example Value**:

```json
{
    "new_password" : string,
    "confirm_new_password" : string
}
```

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

### /api/v1/auth/test-refresh-token

**GET**

**Summary**: Test Refresh Token

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

### /api/v1/project/

**GET**

**Summary**: Get All Projects

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

  - type: array ( $schema: Project )

**Example Value**:

```json
[
    {
        "id" : string,
        "name" : string,
        "description" : string,
        "url" : string,
        "creator_id" : string,
        "creted_at" : string
    }
]
```

**POST**

**Summary**: Create Project

**[ Request Body ]** \*

- application/json:

  - $schema: ProjectCreationModel

**Example Value**:

```json
{
    "name" : string,
    "description" : string,
    "url" : string,
    "creator_id" : string
}
```

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

  - $schema: Project

**Example Value**:

```json
{
    "id" : string,
    "name" : string,
    "description" : string,
    "url" : string,
    "creator_id" : string,
    "creted_at" : string
}
```

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

### /api/v1/project/{project_id}

**GET**

**Summary**: Get Project By Id

**[ Parameters ]**

| name       |  in  | description |  type  | required |
| :--------- | :--: | :---------- | :----: | :------: |
| project_id | path |             | string |    \*    |

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

  - $schema: Project

**Example Value**:

```json
{
    "id" : string,
    "name" : string,
    "description" : string,
    "url" : string,
    "creator_id" : string,
    "creted_at" : string
}
```

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

**PUT**

**Summary**: Update Project

**[ Parameters ]**

| name       |  in  | description |  type  | required |
| :--------- | :--: | :---------- | :----: | :------: |
| project_id | path |             | string |    \*    |

**[ Request Body ]** \*

- application/json:

  - $schema: ProjectUpdateModel

**Example Value**:

```json
{
    "name" : ,
    "description" : ,
    "url" :
}
```

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

  - $schema: Project

**Example Value**:

```json
{
    "id" : string,
    "name" : string,
    "description" : string,
    "url" : string,
    "creator_id" : string,
    "creted_at" : string
}
```

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

**DELETE**

**Summary**: Delete Project

**[ Parameters ]**

| name       |  in   | description |  type  | required |
| :--------- | :---: | :---------- | :----: | :------: |
| project_id | path  |             | string |    \*    |
| auto_error | query |             |        |          |

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

  - $schema: Project

**Example Value**:

```json
{
    "id" : string,
    "name" : string,
    "description" : string,
    "url" : string,
    "creator_id" : string,
    "creted_at" : string
}
```

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

### /api/v1/ideas/

**POST**

**Summary**: Create Idea

**[ Request Body ]** \*

- application/json:

  - $schema: IdeaCreationModel

**Example Value**:

```json
{
    "title" : string,
    "description" : string,
    "category_id" : integer,
    "creator_id" : string,
    "project_id" : string
}
```

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

**GET**

**Summary**: Search Ideas Route

**[ Parameters ]**

| name       |  in   | description | type | required |
| :--------- | :---: | :---------- | :--: | :------: |
| project_id | query |             |      |          |
| text       | query |             |      |          |
| limit      | query |             |      |          |
| cursor     | query |             |      |          |

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

### /api/v1/ideas/{idea_id}

**GET**

**Summary**: Get Idea By Id

**[ Parameters ]**

| name    |  in  | description |  type  | required |
| :------ | :--: | :---------- | :----: | :------: |
| idea_id | path |             | string |    \*    |

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

### /api/v1/ideas/{idea_id}/comment

**POST**

**Summary**: Make Comment

**[ Parameters ]**

| name    |  in  | description |  type  | required |
| :------ | :--: | :---------- | :----: | :------: |
| idea_id | path |             | string |    \*    |

**[ Request Body ]** \*

- application/json:

  - $schema: CommentCreationModel

**Example Value**:

```json
{
    "content" : string,
    "user_id" : string,
    "idea_id" : string
}
```

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

### /api/v1/ideas/{idea_id}/votes

**POST**

**Summary**: Vote

**[ Parameters ]**

| name    |  in  | description |  type  | required |
| :------ | :--: | :---------- | :----: | :------: |
| idea_id | path |             | string |    \*    |

**[ Request Body ]** \*

- application/json:

  - $schema: VoteCreationModel

**Example Value**:

```json
{
    "is_upvote" : boolean
}
```

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

**GET**

**Summary**: Get Votes

**[ Parameters ]**

| name    |  in  | description |  type  | required |
| :------ | :--: | :---------- | :----: | :------: |
| idea_id | path |             | string |    \*    |

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

**DELETE**

**Summary**: Remove Vote

**[ Parameters ]**

| name    |  in  | description |  type  | required |
| :------ | :--: | :---------- | :----: | :------: |
| idea_id | path |             | string |    \*    |

**[ Responses ]**

code: 200

description: Successful Response

- application/json:

code: 422

description: Validation Error

- application/json:

  - $schema: HTTPValidationError

**Example Value**:

```json
{
    "detail" : [
        {
            "loc" : [
            ],
            "msg" : string,
            "type" : string
        }
    ]
}
```

---

### **Components**

### Schemas

**CommentCreationModel**

**content**:

- **string**

  - _required: true_

  - _nullable: false_

**user_id**:

- **string**

  - _format: uuid_

  - _required: true_

  - _nullable: false_

**idea_id**:

- **string**

  - _format: uuid_

  - _required: true_

  - _nullable: false_

**HTTPValidationError**

**detail**:

- **array [ ValidationError ]**

  - _required: false_

  - _nullable: false_

**IdeaCreationModel**

**title**:

- **string**

  - _required: true_

  - _nullable: false_

**description**:

- **string**

  - _required: true_

  - _nullable: false_

**category_id**:

- **integer**

  - _required: true_

  - _nullable: false_

**creator_id**:

- **string**

  - _format: uuid_

  - _required: true_

  - _nullable: false_

**project_id**:

- **string**

  - _format: uuid_

  - _required: true_

  - _nullable: false_

**PasswordResetConfirmModel**

**new_password**:

- **string**

  - _required: true_

  - _nullable: false_

**confirm_new_password**:

- **string**

  - _required: true_

  - _nullable: false_

**PasswordResetRequestModel**

**email**:

- **string**

  - _required: true_

  - _nullable: false_

**Project**

**id**:

- **string**

  - _format: uuid_

  - _required: true_

  - _nullable: false_

**name**:

- **string**

  - _required: true_

  - _nullable: false_

**description**:

- **string**

  - _required: true_

  - _nullable: false_

**url**:

- **string**

  - _required: true_

  - _nullable: false_

**creator_id**:

- **string**

  - _format: uuid_

  - _required: true_

  - _nullable: false_

**creted_at**:

- **string**

  - _format: date-time_

  - _required: true_

  - _nullable: false_

**ProjectCreationModel**

**name**:

- **string**

  - _required: true_

  - _nullable: false_

**description**:

- **string**

  - _required: true_

  - _nullable: false_

**url**:

- **string**

  - _required: true_

  - _nullable: false_

**creator_id**:

- **string**

  - _format: uuid_

  - _required: true_

  - _nullable: false_

**ProjectUpdateModel**

**name**:

    - _required: false_

    - _nullable: false_

**description**:

    - _required: false_

    - _nullable: false_

**url**:

    - _required: false_

    - _nullable: false_

**UserCreateModel**

**username**:

- **string**

  - _required: true_

  - _nullable: false_

  - _maxLength: 25_

**email**:

- **string**

  - _required: true_

  - _nullable: false_

  - _maxLength: 40_

**password**:

- **string**

  - _required: true_

  - _nullable: false_

  - _minLength: 6_

**UserLoginModel**

**email**:

- **string**

  - _required: true_

  - _nullable: false_

  - _maxLength: 40_

**password**:

- **string**

  - _required: true_

  - _nullable: false_

  - _minLength: 6_

**ValidationError**

**loc**:

    - _required: true_

    - _nullable: false_

**msg**:

- **string**

  - _required: true_

  - _nullable: false_

**type**:

- **string**

  - _required: true_

  - _nullable: false_

**VoteCreationModel**

**is_upvote**:

- **boolean**

  - _required: true_

  - _nullable: false_

---

### Security Schemes

**AccessTokenBearer**

- type: http

- scheme: bearer

**OptionalAccessTokenBearer**

- type: http

- scheme: bearer

---
