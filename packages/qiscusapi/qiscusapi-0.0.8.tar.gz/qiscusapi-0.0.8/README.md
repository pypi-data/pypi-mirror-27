Qiscus API Wrapper
==================

Python wrapper for Qiscus SDK [RESTful API](https://www.qiscus.com/docs/restapi). This wrapper allows Qiscus user to manage users, comments, and rooms in Qiscus app. 

## Installation

```python
pip install qiscusapi
```
## Requires
* [requests](https://pypi.python.org/pypi/requests) - Python HTTP for Humans.

## Usage
Initialize the API with your `app_id` and `qiscus_secret_key`:
```python
from qiscusapi.api import Api
api = Api('app_id', 'qiscus_secret_key')
```
Now, you can use available methods:
```python
r = api.login_or_register('your_email', 'your_username', 'your_password'):
print(r.user_id, r.user_email, r.username, r.user_avatar_url, r.user_token)

r = api.get_user_room_lists('user_email')
for rooms in r.rooms_info:
    print(rooms.room_name)
```
## Lists of methods
This is lists of available method in this wrapper. You can also access [docstring](https://www.python.org/dev/peps/pep-0257/) for specific methods. Example:

1. [login or register](#login_or_register-)
2. [check user profile](#check_user_profile-)
3. [get user room lists](#get_user_room_lists-)
4. [create room](#create_room-)
5. [update room](#update_room-)
6. [get or create room with target](#get_or_create_room_with_target-)
7. [get rooms info](#get_rooms_info-)
8. [add room participants](#add_room_participants-)
9. [remove room participants](#remove_room_participants-)
10. [post comment text](#post_comment_text-)
11. [post comment buttons](#post_comment_buttons-)
12. [post comment card](#post_comment_card-)
13. [post comment postback button](#post_comment_postback_button-)
14. [post comment account linking](#post_comment_account_linking-)
15. [post comment custom](#post_comment_custom-)
16. [load comments](#load_comments-)
17. [search messages](#search_messages-)
18. [post system event message](#post_system_event_message-)
17. [error status](#Error)


```python
help(get_user_room_lists)
```

### login_or_register:

```python
Accepted parameters:

email [required]
username [required]
password [optional]
avatar_url [optional]
device_token [optional]
device_platform ["ios" or "android", optional]

Callable objects:

user_id
user_email
username
user_avatar_url
user_token
user_info_as_json
```

### check_user_profile:
```python
Accepted parameters:

user_email [required]

Callable objects:

user_id
user_email
username
user_avatar_url
user_token
user_info_as_json
```

### get_user_room_lists:
```python
Accepted parameters:

user_email [required]
page [optional] number of page
show_participants [optional] "true" or "false" default will be false
room_type [optional]

Callable objects:

rooms_info[].last_comment_id
rooms_info[].last_comment_message
rooms_info[].last_comment_timestamp
rooms_info[].avatar_url
rooms_info[].room_id
rooms_info[].room_name
rooms_info[].room_type
rooms_info[].unread_count
rooms_info[].info_as_json
rooms_info_as_json
```

### create_room:
```python
Accepted parameters:

name [required]
creator [required]
participants[] [required]
avatar_url [optional]

Callable objects:

room_creator
room_id
room_name
room_type
room_info_as_json
room_participants[].avatar_url
room_participants[].email
room_participants[].participants_id
room_participants[].last_comment_read_id
room_participants[].last_comment_received_id
room_participants[].username
room_participants[].info_as_json
```

### update_room:
```python
Accepted parameters:

user_email [required] must one of user participant
room_id [required] must be group room
room_name [optional]
room_avatar_url [optional]
options [optional]

Callable objects:

room_chat_type
room_id
room_last_comment_id
room_last_comment_message
room_last_topic_id
room_avatar_url
room_name
room_participants[].avatar_url
room_participants[].email
room_participants[].username
room_participants[].last_comment_read_id
room_participants[].last_comment_received_id
room_participants[].info_as_json
room_comments[].comments_id
room_comments[].comments_before_id
room_comments[].message
room_comments[].type
room_comments[].payload
room_comments[].disable_link_preview
room_comments[].email
room_comments[].username
room_comments[].user_avatar_url
room_comments[].timestamp
room_comments[].unix_timestamp
room_comments[].unique_temp_id
room_comments[].info_as_json
room_info_as_json
```

### get_or_create_room_with_target:
```python
Accepted parameters:

email1 [required]
email2 [required]

Callable objects:

room_avatar_url
room_chat_type
room_id
room_last_comment_id
room_last_comment_message
room_last_topic_id
room_options
room_name
room_info_as_json
room_comments[].comments_before_id
room_comments[].disable_link_preview
room_comments[].email
room_comments[].comments_id
room_comments[].message
room_comments[].timestamp
room_comments[].unique_temp_id
room_comments[].user_avatar_url
room_comments[].username
room_comments[].info_as_json
room_participants[].avatar_url
room_participants[].email
room_participants[].username
room_participants[].info_as_json
```

### get_rooms_info:
```python
Accepted parameters:

user_email [required]
room_id[] [required, array of string]
show_participants [required boolean, true or false, default is false]
```

### add_room_participants:
```python
Accepted parameters:

room_id [required]
emails[] [required, array of string emails]

Callable objects:

room_creator
room_participants
room_id
room_name
room_type
room_info_as_json
```

### remove_room_participants:
```python
Accepted parameters:

room_id [required]
emails [required, array of string emails]

Callable object:

room_creator
room_participants
room_id
room_name
room_type
room_info_as_json
```

### post_comment_text:
```python
Accepted parameters:

sender_email [required]
room_id [required], it can be room_id or channel id specified by client or auto generated by server
message [required]
payload [required, string json]
unique_temp_id [optional, default=generated by backend]
disable_link_preview [optional, default=false]

Callable objects:

room_creator
room_participants
room_id
room_name
room_type
room_info_as_json
```

### post_comment_buttons:
```python
Accepted parameters:

sender_email [required]
room_id [required], it can be room_id or channel id specified by client or auto generated by server
payload [required, string json]

Callable objects:

comment_payload
comment_room_id
comment_timestamp
comment_topic_id
comment_type
comment_unique_temp_id
comment_unix_nano_timestamp
comment_unix_timestamp
comment_user_avatar_url
comment_user_id
comment_username
comment_before_id
comment_disable_link_preview
comment_email
comment_id
comment_message
comment_payload_text
comment_info_as_json
comment_payload_buttons[].label
comment_payload_buttons[].type
comment_payload_buttons[].payload
comment_payload_buttons[].info_as_json
```

### post_comment_card:
```python
Accepted parameters:

sender_email [required]
room_id [required], it can be room_id or channel id specified by client or auto generated by server
payload [required, string json, see payload example at Qiscus documentation]

Callable objects:

comment_before_id
comment_disable_link_preview
comment_user_email
comment_id
comment_message
comment_payload
comment_payload_description
comment_payload_image
comment_payload_text
comment_payload_title
comment_payload_url
comment_room_id
comment_status
comment_timestamp
comment_topic_id
comment_user_avatar_url
comment_user_id
comment_username
comment_info_as_json
```

### post_comment_postback_button:
```python
Accepted parameters:

sender_email [required]
room_id [required], it can be room_id or channel id specified by client or auto generated by server
payload [required, json, see payload example at Qiscus documentation]

Callable objects:

comment_before_id
comment_disable_link_preview
comment_email
comment_extras
comment_id
comment_message
comment_payload
payload_url
payload_method
payload_payload
comment_room_id
comment_status
comment_timestamp
comment_topic_id
comment_type
comment_unique_temp_id
comment_unix_nano_timestamp
comment_unix_timestamp
comment_user_avatar_url
comment_user_id
comment_username
comment_info_as_json
```

### post_comment_account_linking:
```python
Accepted parameters:

sender_email [required]
room_id [required], it can be room_id or channel id specified by client or auto generated by server
payload [required json, see payload example at Qiscus documentation]

Callable objects:

comment_message
comment_user_avatar_url
comment_before_id_str
comment_user_id
comment_disable_link_preview
comment_unix_nano_timestamp
comment_topic_id
comment_type
comment_id
comment_extras
comment_unix_timestamp
comment_payload
payload_url
payload_redirect_url
payload_text
payload_params
payload_params_topic_id
payload_params_user_id
payload_params_button_text
payload_params_view_title
payload_params_success_message
comment_before_id
comment_username
comment_timestamp
comment_email
comment_room_id
comment_status
comment_unique_temp_id
comment_info_as_json
```

### post_comment_custom:
```python
Accepted parameters:

sender_email [required]
room_id [required], it can be room_id or channel id specified by client or auto generated by server
payload [required json, see payload example at Qiscus documentation]

Callable objects:

comment_before_id
comment_disable_link_preview
comment_user_email
comment_id
comment_message
comment_payload
comment_room_id
comment_status
comment_timestamp
comment_topic_id
comment_user_avatar_url
comment_user_id
comment_username
comment_info_as_json
```

### load_comments:
```python
Accepted parameters:

room_id [required]
page [optional]
limit [optional default=20]

Callable objects:

comments_info[].comment_before_id
comments_info[].disable_link_preview
comments_info[].user_email
comments_info[].comments_id
comments_info[].message
comments_info[].room_id
comments_info[].room_name
comments_info[].timestamp
comments_info[].unique_temp_id
comments_info[].user_avatar_url
comments_info[].username
comments_info[].info_as_json
```

### search_messages:
```python

Accepted Parameters:

user_email [required]
query [required], keyword to search
room_id [optional], send this param if you want search message in specific room


Callable objects:

messages_info[].chat_type
messages_info[].comment_before_id
messages_info[].disable_link_preview
messages_info[].user_email
messages_info[].comments_id
messages_info[].message
messages_info[].payload
messages_info[].room_id
messages_info[].room_name
messages_info[].timestamp
messages_info[].topic_id
messages_info[].type
messages_info[].unique_temp_id
messages_info[].unix_timestamp
messages_info[].user_avatar_url
messages_info[].user_id
messages_info[].username
messages_info[].info_as_json
messages_info_as_json
```
### post_system_event_message:
```python
system_event_type [required] valid value is: "create_room", "add_member", "join_room", "remove_member", "left_room", "change_room_name", "change_room_avatar"
room_id [required] room id to post
subject_email [required] person who create a room, add member to room, join room, remove member from room, left from room, change room name and/or room avatar
object_email[] [optional, array of string] optional, only required when system event type is add_member or remove_member
updated_room_name [optional] only required when system event message type is change_room_name or create_room

```

### Error:
```python
All methods in this wrapper using same objects name that you can call.

error_message
error_info_as_json
error_status_code
```

## Further Information
For more information, please check RESTful API Qiscus [documentation](https://www.qiscus.com/docs/restapi)
