
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from dubious.discord.disc import Disc, Snowflake

@dataclass
class ApplicationCommand(Disc):
    # Unique ID of command                                                                                                                                              
    id: Snowflake
    # `Type of command`, defaults to `1`                                  
    type:  ApplicationCommandType | None = field(kw_only=True, default=None)
    # ID of the parent application                                                                                                                                      
    application_id: Snowflake
    # guild id of the command, if not global                                                                                                                            
    guild_id: Snowflake | None = field(kw_only=True, default=None)
    # `Name of command`, 1-32 characters                                 
    name: str
    # Localization dictionary for `name` field. Values follow the same restrictions as `name`                                                                           
    name_localizations: dict[str, str] | None = field(kw_only=True, default=None)
    # Description for `CHAT_INPUT` commands, 1-100 characters. Empty string for `USER` and `MESSAGE` commands                                                           
    description: str
    # Localization dictionary for `description` field. Values follow the same restrictions as `description`                                                             
    description_localizations: dict[str, str] | None = field(kw_only=True, default=None)
    # Parameters for the command, max of 25                                                                                                                             
    options: list[ApplicationCommandOption] | None = field(kw_only=True, default=None)
    # Set of `permissions` represented as a bit set                                                                                           
    default_member_permissions: str | None
    # Indicates whether the command is available in DMs with the app, only for globally-scoped commands. By default, commands are visible.                              
    dm_permission: bool | None = field(kw_only=True, default=None)
    # Not recommended for use as field will soon be deprecated. Indicates whether the command is enabled by default when the app is added to a guild, defaults to `true`
    default_permission: bool | None = field(kw_only=True, default=None)
    # Autoincrementing version identifier updated during substantial record changes                                                                                     
    version: Snowflake

class ApplicationCommandType(int, Enum):
    # Slash commands; a text-based command that shows up when a user types `/`
    CHAT_INPUT = 1
    # A UI-based command that shows up when you right click or tap on a user
    USER = 2
    # A UI-based command that shows up when you right click or tap on a message
    MESSAGE = 3

@dataclass
class ApplicationCommandOption(Disc):
    # Type of option                                                                                                      
    type:  ApplicationCommandOptionType
    # `1-32 character name`
    name: str
    # Localization dictionary for the `name` field. Values follow the same restrictions as `name`                         
    name_localizations: dict[str, str] | None = field(kw_only=True, default=None)
    # 1-100 character description                                                                                         
    description: str
    # Localization dictionary for the `description` field. Values follow the same restrictions as `description`           
    description_localizations: dict[str, str] | None = field(kw_only=True, default=None)
    # If the parameter is required or optional--default `false`                                                           
    required: bool | None = field(kw_only=True, default=None)
    # Choices for `STRING`, `INTEGER`, and `NUMBER` types for the user to pick from, max 25                               
    choices: list[ApplicationCommandOptionChoice] | None = field(kw_only=True, default=None)
    # If the option is a subcommand or subcommand group type, these nested options will be the parameters                 
    options: list[ApplicationCommandOption] | None = field(kw_only=True, default=None)
    # If the option is a channel type, the channels shown will be restricted to these types                               
    channel_types: list[ChannelType] | None = field(kw_only=True, default=None)
    # If the option is an `INTEGER` or `NUMBER` type, the minimum value permitted                                         
    min_value: int | float | None = field(kw_only=True, default=None)
    # If the option is an `INTEGER` or `NUMBER` type, the maximum value permitted                                         
    max_value: int | float | None = field(kw_only=True, default=None)
    # For option type `STRING`, the minimum allowed length (minimum of `0`, maximum of `6000`)                            
    min_length: int | None = field(kw_only=True, default=None)
    # For option type `STRING`, the maximum allowed length (minimum of `1`, maximum of `6000`)                            
    max_length: int | None = field(kw_only=True, default=None)
    # If autocomplete interactions are enabled for this `STRING`, `INTEGER`, or `NUMBER` type option                      
    autocomplete: bool | None = field(kw_only=True, default=None)

class ApplicationCommandOptionType(int, Enum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    # Any integer between -2^53 and 2^53
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    # Includes all channel types + categories
    CHANNEL = 7
    ROLE = 8
    # Includes users and roles
    MENTIONABLE = 9
    # Any double between -2^53 and 2^53
    NUMBER = 10
    # `attachment` object
    ATTACHMENT = 11

@dataclass
class ApplicationCommandOptionChoice(Disc):
    # 1-100 character choice name                                                                
    name: str
    # Localization dictionary for the `name` field. Values follow the same restrictions as `name`
    name_localizations: dict[str, str] | None = field(kw_only=True, default=None)
    # Value for the choice, up to 100 characters if string                                       
    value: str | int | float 

@dataclass
class GuildApplicationCommandPermissions(Disc):
    # ID of the command or the application ID             
    id: Snowflake
    # ID of the application the command belongs to        
    application_id: Snowflake
    # ID of the guild                                     
    guild_id: Snowflake
    # Permissions for the command in the guild, max of 100
    permissions: list[ApplicationCommandPermission]

@dataclass
class ApplicationCommandPermission(Disc):
    # ID of the role, user, or channel. It can also be a `permission constant`
    id: Snowflake
    # role (`1`), user (`2`), or channel (`3`)                                                                                                                                                          
    type: ApplicationCommandPermissionType
    # `true` to allow, `false`, to disallow                                                                                                                                                             
    permission: bool

class ApplicationCommandPermissionType(int, Enum):
    ROLE = 1
    USER = 2
    CHANNEL = 3

@dataclass
class Interaction(Disc):
    # ID of the interaction                                                                         
    id: Snowflake
    # ID of the application this interaction is for                                                 
    application_id: Snowflake
    # Type of interaction                                                                           
    type: InteractionType
    # Interaction data payload                                                                      
    data: InteractionData | None = field(kw_only=True, default=None)
    # Guild that the interaction was sent from                                                      
    guild_id: Snowflake | None = field(kw_only=True, default=None)
    # Channel that the interaction was sent from                                                    
    channel_id: Snowflake | None = field(kw_only=True, default=None)
    # Guild member data for the invoking user, including permissions                                
    member: GuildMember | None = field(kw_only=True, default=None)
    # User object for the invoking user, if invoked in a DM                                         
    user: User | None = field(kw_only=True, default=None)
    # Continuation token for responding to the interaction                                          
    token: str
    # Read-only property, always `1`                                                                
    version: int
    # For components, the message they were attached to                                             
    message: Message | None = field(kw_only=True, default=None)
    # Bitwise set of permissions the app or bot has within the channel the interaction was sent from
    app_permissions: str | None = field(kw_only=True, default=None)
    # Selected `language` of the invoking user                             
    locale: str | None = field(kw_only=True, default=None)
    # `Guild's preferred locale`, if invoked in a guild         
    guild_locale: str | None = field(kw_only=True, default=None)

class InteractionType(int, Enum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5

@dataclass
class ApplicationCommandData(Disc):
    # the ``ID`` of the invoked command                                                 
    id: Snowflake
    # the ``name`` of the invoked command                                               
    name: str
    # the ``type`` of the invoked command                                               
    type: int
    # converted users + roles + channels + attachments                                                                                                                                    
    resolved: ResolvedData | None = field(kw_only=True, default=None)
    # the params + values from the user                                                                                                                                                   
    options: list[ApplicationCommandInteractionDataOption] | None = field(kw_only=True, default=None)
    # the id of the guild the command is registered to                                                                                                                                    
    guild_id: Snowflake | None = field(kw_only=True, default=None)
    # id of the user or message targeted by a `user` command
    target_id: Snowflake | None = field(kw_only=True, default=None)

@dataclass
class MessageComponentData(Disc):
    # the ``custom_id`` of the component                            
    custom_id: str
    # the `type` of the component            
    component_type: int
    # values the user selected in a `select menu` component
    values: list[SelectOption] | None = field(kw_only=True, default=None)

@dataclass
class ModalSubmitData(Disc):
    # the ``custom_id`` of the modal
    custom_id: str
    # the values submitted by the user                                               
    components: list[MessageComponent]

@dataclass
class ResolvedData(Disc):
    # the ids and User objects           
    users: dict[Snowflake, User] | None = field(kw_only=True, default=None)
    # the ids and partial Member objects 
    members: dict[Snowflake, GuildMember] | None = field(kw_only=True, default=None)
    # the ids and Role objects           
    roles: dict[Snowflake, Role] | None = field(kw_only=True, default=None)
    # the ids and partial Channel objects
    channels: dict[Snowflake, Channel] | None = field(kw_only=True, default=None)
    # the ids and partial Message objects
    messages: dict[Snowflake, Message] | None = field(kw_only=True, default=None)
    # the ids and attachment objects     
    attachments: dict[Snowflake, Attachment] | None = field(kw_only=True, default=None)

@dataclass
class ApplicationCommandInteractionDataOption(Disc):
    # Name of the parameter                                                                                                                         
    name: str
    # Value of `application command option type`
    type: int
    # Value of the option resulting from user input                                                                                                 
    value: str | int | float | None = field(kw_only=True, default=None)
    # Present if this option is a group or subcommand                                                                                               
    options: list[ApplicationCommandInteractionDataOption] | None = field(kw_only=True, default=None)
    # `true` if this option is the currently focused option for autocomplete                                                                        
    focused: bool | None = field(kw_only=True, default=None)

@dataclass
class MessageInteraction(Disc):
    # ID of the interaction                                                                                                                                                           
    id: Snowflake
    # Type of interaction                                                                                                                                                             
    type: InteractionType
    # Name of the `application command`, including subcommands and subcommand groups
    name: str
    # User who invoked the interaction                                                                                                                                                
    user: User
    # Member who invoked the interaction in the guild                                                                                                                                 
    member: GuildMember | None = field(kw_only=True, default=None)

@dataclass
class InteractionResponse(Disc):
    # the type of response        
    type: InteractionCallbackType
    # an optional response message
    data: InteractionCallbackData | None = field(kw_only=True, default=None)

class InteractionCallbackType(int, Enum):
    # ACK a `Ping`
    PONG = 1
    # respond to an interaction with a message
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    # ACK an interaction and edit a response later, the user sees a loading state
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    # for components, ACK an interaction and edit the original message later; the user does not see a loading state
    DEFERRED_UPDATE_MESSAGE = 6
    # for components, edit the message the component was attached to
    UPDATE_MESSAGE = 7
    # respond to an autocomplete interaction with suggested choices
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
    # respond to an interaction with a popup modal
    MODAL = 9

@dataclass
class ResponseMessage(Disc):
    # is the response TTS                                                                                                                                                                        
    tts: bool | None = field(kw_only=True, default=None)
    # message content                                                                                                                                                                            
    content: str | None = field(kw_only=True, default=None)
    # supports up to 10 embeds                                                                                                                                                                   
    embeds: list[Embed] | None = field(kw_only=True, default=None)
    # `allowed mentions` object                                                                                                                 
    allowed_mentions: AllowedMentions | None = field(kw_only=True, default=None)
    # `message flags`
    flags: int | None = field(kw_only=True, default=None)
    # message components                                                                                                                                                                         
    components: list[MessageComponent] | None = field(kw_only=True, default=None)
    # attachment objects with filename and description                                                                                                                                           
    attachments: list[Attachment] | None = field(kw_only=True, default=None)

@dataclass
class ResponseAutocomplete(Disc):
    # autocomplete choices (max of 25 choices)
    choices: list[ApplicationCommandOptionChoice]

@dataclass
class ResponseModal(Disc):
    # a developer-defined identifier for the component, max 100 characters
    custom_id: str
    # the title of the popup modal, max 45 characters                     
    title: str
    # between 1 and 5 (inclusive) components that make up the modal       
    components: list[MessageComponent]

class ComponentType(int, Enum):
    # A container for other components
    ACTION_ROW = 1
    # A button object
    BUTTON = 2
    # A select menu for picking from choices
    SELECT_MENU = 3
    # A text input object
    TEXT_INPUT = 4

@dataclass
class ActionRow(Disc):
    # `1` for an action row     
    type: int = field(kw_only=True, default=1)
    # the components on this row
    components: list[MessageComponent]

@dataclass
class Button(Disc):
    # `2` for a button                                                                         
    type: int = field(kw_only=True, default=2)
    # one of `button styles`
    style: int
    # text that appears on the button, max 80 characters                                       
    label: str | None = field(kw_only=True, default=None)
    # `name`, `id`, and `animated`                                                             
    emoji: Emoji | None = field(kw_only=True, default=None)
    # a developer-defined identifier for the button, max 100 characters                        
    custom_id: str | None = field(kw_only=True, default=None)
    # a url for link-style buttons                                                             
    url: str | None = field(kw_only=True, default=None)
    # whether the button is disabled (default `false`)                                         
    disabled: bool | None = field(kw_only=True, default=None)

class ButtonStyle(int, Enum):
    # blurple                  | `custom_id`
    PRIMARY = 1
    # grey                     | `custom_id`
    SECONDARY = 2
    # green                    | `custom_id`
    SUCCESS = 3
    # red                      | `custom_id`
    DANGER = 4
    # grey, navigates to a URL | `url`
    LINK = 5

@dataclass
class SelectMenu(Disc):
    # `3` for a select menu                                                    
    type: int = field(kw_only=True, default=3)
    # a developer-defined identifier for the select menu, max 100 characters   
    custom_id: str
    # the choices in the select, max 25                                        
    options: list[SelectOption]
    # custom placeholder text if nothing is selected, max 150 characters       
    placeholder: str | None = field(kw_only=True, default=None)
    # the minimum number of items that must be chosen; default 1, min 0, max 25
    min_values: int | None = field(kw_only=True, default=None)
    # the maximum number of items that can be chosen; default 1, max 25        
    max_values: int | None = field(kw_only=True, default=None)
    # disable the select, default false                                        
    disabled: bool | None = field(kw_only=True, default=None)

@dataclass
class SelectOption(Disc):
    # the user-facing name of the option, max 100 characters     
    label: str
    # the dev-defined value of the option, max 100 characters    
    value: str
    # an additional description of the option, max 100 characters
    description: str | None = field(kw_only=True, default=None)
    # `id`, `name`, and `animated`                               
    emoji: Emoji | None = field(kw_only=True, default=None)
    # will render this option as selected by default             
    default: bool | None = field(kw_only=True, default=None)

@dataclass
class TextInput(Disc):
    # `4` for a text input                                                                       
    type: int = field(kw_only=True, default=4)
    # a developer-defined identifier for the input, max 100 characters                           
    custom_id: str
    # the `Text Input Style`
    style: int
    # the label for this component, max 45 characters                                            
    label: str
    # the minimum input length for a text input, min 0, max 4000                                 
    min_length: int | None = field(kw_only=True, default=None)
    # the maximum input length for a text input, min 1, max 4000                                 
    max_length: int | None = field(kw_only=True, default=None)
    # whether this component is required to be filled, default true                              
    required: bool | None = field(kw_only=True, default=None)
    # a pre-filled value for this component, max 4000 characters                                 
    value: str | None = field(kw_only=True, default=None)
    # custom placeholder text if the input is empty, max 100 characters                          
    placeholder: str | None = field(kw_only=True, default=None)

class TextInputStyle(int, Enum):
    # A single-line input
    SHORT = 1
    # A multi-line input
    PARAGRAPH = 2

@dataclass
class StageInstance(Disc):
    # The id of this Stage instance                                                                                
    id: Snowflake
    # The guild id of the associated Stage channel                                                                 
    guild_id: Snowflake
    # The id of the associated Stage channel                                                                       
    channel_id: Snowflake
    # The topic of the Stage instance (1-120 characters)                                                           
    topic: str
    # The `privacy level` of the Stage instance
    privacy_level: int
    # Whether or not Stage Discovery is disabled (deprecated)                                                      
    discoverable_disabled: bool
    # The id of the scheduled event for this Stage instance                                                        
    guild_scheduled_event_id: Snowflake | None

class PrivacyLevel(int, Enum):
    # The Stage instance is visible publicly. (deprecated)
    PUBLIC = 1
    # The Stage instance is visible to only guild members.
    GUILD_ONLY = 2

@dataclass
class AutoModerationRule(Disc):
    # the id of this rule                                                                                      
    id: Snowflake
    # the id of the guild which this rule belongs to                                                           
    guild_id: Snowflake
    # the rule name                                                                                            
    name: str
    # the user which first created this rule                                                                   
    creator_id: Snowflake
    # the rule `event type`           
    event_type: int
    # the rule `trigger type`       
    trigger_type: int
    # the rule `trigger metadata`
    trigger_metadata: object
    # the actions which will execute when the rule is triggered                                                
    actions: list[AutoModerationAction]
    # whether the rule is enabled                                                                              
    enabled: bool
    # the role ids that should not be affected by the rule (Maximum of 20)                                     
    exempt_roles: list[Snowflake]
    # the channel ids that should not be affected by the rule (Maximum of 50)                                  
    exempt_channels: list[Snowflake]

class TriggerType(int, Enum):
    # check if content contains words from a user defined list of keywords | 3
    KEYWORD = 1
    # check if content represents generic spam                             | 1
    SPAM = 3
    # check if content contains words from internal pre-defined wordsets   | 1
    KEYWORD_PRESET = 4
    # check if content contains more unique mentions than allowed          | 1
    MENTION_SPAM = 5

class KeywordPresetType(int, Enum):
    # Words that may be considered forms of swearing or cursing
    PROFANITY = 1
    # Words that refer to sexually explicit behavior or activity
    SEXUAL_CONTENT = 2
    # Personal insults or words that may be considered hate speech
    SLURS = 3

class EventType(int, Enum):
    # when a member sends or edits a message in the guild
    MESSAGE_SEND = 1

@dataclass
class AutoModerationAction(Disc):
    # the type of action                                                       
    type: AutoModerationActionType
    # additional metadata needed during execution for this specific action type
    metadata: AutoModerationActionMetadata | None = field(kw_only=True, default=None)

class AutoModerationActionType(int, Enum):
    # blocks the content of a message according to the rule
    BLOCK_MESSAGE = 1
    # logs user content to a specified channel
    SEND_ALERT_MESSAGE = 2
    # timeout user for a specified duration *
    TIMEOUT = 3

@dataclass
class AutoModerationActionMetadata(Disc):
    # SEND_ALERT_MESSAGE     
    channel_id: Snowflake
    # TIMEOUT                
    duration_seconds: int

@dataclass
class Channel(Disc):
    # the id of this channel                                                                                                                                                                       
    id: Snowflake
    # the `type of channel`                                                                                                                  
    type: int
    # the id of the guild (may be missing for some channel objects received over gateway guild dispatches)                                                                                         
    guild_id: Snowflake | None = field(kw_only=True, default=None)
    # sorting position of the channel                                                                                                                                                              
    position: int | None = field(kw_only=True, default=None)
    # explicit permission overwrites for members and roles                                                                                                                                         
    permission_overwrites: list[Overwrite] | None = field(kw_only=True, default=None)
    # the name of the channel (1-100 characters)                                                                                                                                                   
    name: str | None = field(kw_only=True, default=None)
    # the channel topic (0-4096 characters for `GUILD_FORUM` channels, 0-1024 characters for all others)                                                                                           
    topic: str | None = field(kw_only=True, default=None)
    # whether the channel is nsfw                                                                                                                                                                  
    nsfw: bool | None = field(kw_only=True, default=None)
    # the id of the last message sent in this channel (or thread for `GUILD_FORUM` channels) (may not point to an existing or valid message or thread)                                             
    last_message_id: Snowflake | None = field(kw_only=True, default=None)
    # the bitrate (in bits) of the voice channel                                                                                                                                                   
    bitrate: int | None = field(kw_only=True, default=None)
    # the user limit of the voice channel                                                                                                                                                          
    user_limit: int | None = field(kw_only=True, default=None)
    # amount of seconds a user has to wait before sending another message (0-21600); bots, as well as users with the permission `manage_messages` or `manage_channel`, are unaffected              
    rate_limit_per_user: int | None = field(kw_only=True, default=None)
    # the recipients of the DM                                                                                                                                                                     
    recipients: list[User] | None = field(kw_only=True, default=None)
    # icon hash of the group DM                                                                                                                                                                    
    icon: str | None = field(kw_only=True, default=None)
    # id of the creator of the group DM or thread                                                                                                                                                  
    owner_id: Snowflake | None = field(kw_only=True, default=None)
    # application id of the group DM creator if it is bot-created                                                                                                                                  
    application_id: Snowflake | None = field(kw_only=True, default=None)
    # for guild channels: id of the parent category for a channel (each parent category can contain up to 50 channels), for threads: id of the text channel this thread was created                
    parent_id: Snowflake | None = field(kw_only=True, default=None)
    # when the last pinned message was pinned. This may be `null` in events such as `GUILD_CREATE` when a message is not pinned.                                                                   
    last_pin_timestamp: str | None = field(kw_only=True, default=None)
    # `voice region` id for the voice channel, automatic when set to null                                                                               
    rtc_region: str | None = field(kw_only=True, default=None)
    # the camera `video quality mode` of the voice channel, 1 when not present                                                         
    video_quality_mode: int | None = field(kw_only=True, default=None)
    # number of messages (not including the initial message or deleted messages) in a thread.                                                                                                      
    message_count: int | None = field(kw_only=True, default=None)
    # an approximate count of users in a thread, stops counting at 50                                                                                                                              
    member_count: int | None = field(kw_only=True, default=None)
    # thread-specific fields not needed by other channels                                                                                                                                          
    thread_metadata: ThreadMetadata | None = field(kw_only=True, default=None)
    # thread member object for the current user, if they have joined the thread, only included on certain API endpoints                                                                            
    member: ThreadMember | None = field(kw_only=True, default=None)
    # default duration, copied onto newly created threads, in minutes, threads will stop showing in the channel list after the specified period of inactivity, can be set to: 60, 1440, 4320, 10080
    default_auto_archive_duration: int | None = field(kw_only=True, default=None)
    # computed permissions for the invoking user in the channel, including overwrites, only included when part of the `resolved` data received on a slash command interaction                      
    permissions: str | None = field(kw_only=True, default=None)
    # `channel flags`                                                      
    flags: int | None = field(kw_only=True, default=None)
    # number of messages ever sent in a thread, it's similar to `message_count` on message creation, but will not decrement the number when a message is deleted                                   
    total_message_sent: int | None = field(kw_only=True, default=None)
    # the set of tags that can be used in a `GUILD_FORUM` channel                                                                                                                                  
    available_tags: list[ForumTag] | None = field(kw_only=True, default=None)
    # the IDs of the set of tags that have been applied to a thread in a `GUILD_FORUM` channel                                                                                                     
    applied_tags: list[Snowflake] | None = field(kw_only=True, default=None)
    # the emoji to show in the add reaction button on a thread in a `GUILD_FORUM` channel                                                                                                          
    default_reaction_emoji: DefaultReaction | None = field(kw_only=True, default=None)
    # the initial `rate_limit_per_user` to set on newly created threads in a channel. this field is copied to the thread at creation time and does not live update.                                
    default_thread_rate_limit_per_user: int | None = field(kw_only=True, default=None)
    # the `default sort order type` used to order posts in `GUILD_FORUM` channels. Defaults to `null`, which indicates a preferred sort order hasn't been set by a channel admin 
    default_sort_order: int | None = field(kw_only=True, default=None)

class ChannelType(int, Enum):
    # a text channel within a server
    GUILD_TEXT = 0
    # a direct message between users
    DM = 1
    # a voice channel within a server
    GUILD_VOICE = 2
    # a direct message between multiple users
    GROUP_DM = 3
    # an `organizational category` that contains up to 50 channels
    GUILD_CATEGORY = 4
    # a channel that `users can follow and crosspost into their own server`
    GUILD_ANNOUNCEMENT = 5
    # a temporary sub-channel within a GUILD_ANNOUNCEMENT channel
    ANNOUNCEMENT_THREAD = 10
    # a temporary sub-channel within a GUILD_TEXT channel
    PUBLIC_THREAD = 11
    # a temporary sub-channel within a GUILD_TEXT channel that is only viewable by those invited and those with the MANAGE_THREADS permission
    PRIVATE_THREAD = 12
    # a voice channel for `hosting events with an audience`
    GUILD_STAGE_VOICE = 13
    # the channel in a `hub` containing the listed servers
    GUILD_DIRECTORY = 14
    # Channel that can only contain threads
    GUILD_FORUM = 15

class ChannelFlag(int, Enum):
    # this thread is pinned to the top of its parent `GUILD_FORUM` channel
    PINNED = 1 << 1
    # whether a tag is required to be specified when creating a thread in a `GUILD_FORUM` channel. Tags are specified in the `applied_tags` field.
    REQUIRE_TAG = 1 << 4

class SortOrderType(int, Enum):
    # Sort forum posts by activity
    LATEST_ACTIVITY = 0
    # Sort forum posts by creation time (from most recent to oldest)
    CREATION_DATE = 1

@dataclass
class Message(Disc):
    # id of the message                                                                                                                                                                                                                                                       
    id: Snowflake
    # id of the channel the message was sent in                                                                                                                                                                                                                               
    channel_id: Snowflake
    # the author of this message (not guaranteed to be a valid user, see below)                                                                                                                                                                                               
    author: User
    # contents of the message                                                                                                                                                                                                                                                 
    content: str
    # when this message was sent                                                                                                                                                                                                                                              
    timestamp: str
    # when this message was edited (or null if never)                                                                                                                                                                                                                         
    edited_timestamp: str | None
    # whether this was a TTS message                                                                                                                                                                                                                                          
    tts: bool
    # whether this message mentions everyone                                                                                                                                                                                                                                  
    mention_everyone: bool
    # users specifically mentioned in the message                                                                                                                                                                                                                             
    mentions: list[User]
    # roles specifically mentioned in this message                                                                                                                                                                                                                            
    mention_roles: list[Role]
    # channels specifically mentioned in this message                                                                                                                                                                                                                         
    mention_channels: list[ChannelMention] | None = field(kw_only=True, default=None)
    # any attached files                                                                                                                                                                                                                                                      
    attachments: list[Attachment]
    # any embedded content                                                                                                                                                                                                                                                    
    embeds: list[Embed]
    # reactions to the message                                                                                                                                                                                                                                                
    reactions: list[Reaction] | None = field(kw_only=True, default=None)
    # used for validating a message was sent                                                                                                                                                                                                                                  
    nonce: int | str | None = field(kw_only=True, default=None)
    # whether this message is pinned                                                                                                                                                                                                                                          
    pinned: bool
    # if the message is generated by a webhook, this is the webhook's id                                                                                                                                                                                                      
    webhook_id: Snowflake | None = field(kw_only=True, default=None)
    # `type of message`                                                                                                                                                                                                 
    type: int
    # sent with Rich Presence-related chat embeds                                                                                                                                                                                                                             
    activity: MessageActivity | None = field(kw_only=True, default=None)
    # sent with Rich Presence-related chat embeds                                                                                                                                                                                                                             
    application: Application | None = field(kw_only=True, default=None)
    # if the message is an `Interaction` or application-owned webhook, this is the id of the application                                                                                                                        
    application_id: Snowflake | None = field(kw_only=True, default=None)
    # data showing the source of a crosspost, channel follow add, pin, or reply message                                                                                                                                                                                       
    message_reference: MessageReference | None = field(kw_only=True, default=None)
    # `message flags`                                                                                                                                 
    flags: int | None = field(kw_only=True, default=None)
    # the message associated with the message_reference                                                                                                                                                                                                                       
    referenced_message: Message | None = field(kw_only=True, default=None)
    # sent if the message is a response to an `Interaction`                                                                                                                                                                     
    interaction: MessageInteraction | None = field(kw_only=True, default=None)
    # the thread that was started from this message, includes `thread member` object                                                                                                                                            
    thread: Channel | None = field(kw_only=True, default=None)
    # sent if the message contains components like buttons, action rows, or other interactive components                                                                                                                                                                      
    components: list[MessageComponent] | None = field(kw_only=True, default=None)
    # sent if the message contains stickers                                                                                                                                                                                                                                   
    sticker_items: list[StickerItem] | None = field(kw_only=True, default=None)
    # **Deprecated** the stickers sent with the message                                                                                                                                                                                                                       
    stickers: list[Sticker] | None = field(kw_only=True, default=None)
    # A generally increasing integer (there may be gaps or duplicates) that represents the approximate position of the message in a thread, it can be used to estimate the relative position of the messsage in a thread in company with `total_message_sent` on parent thread
    position: int | None = field(kw_only=True, default=None)

class MessageType(int, Enum):
    # true
    DEFAULT = 0
    # false
    RECIPIENT_ADD = 1
    # false
    RECIPIENT_REMOVE = 2
    # false
    CALL = 3
    # false
    CHANNEL_NAME_CHANGE = 4
    # false
    CHANNEL_ICON_CHANGE = 5
    # true
    CHANNEL_PINNED_MESSAGE = 6
    # true
    USER_JOIN = 7
    # true
    GUILD_BOOST = 8
    # true
    GUILD_BOOST_TIER_1 = 9
    # true
    GUILD_BOOST_TIER_2 = 10
    # true
    GUILD_BOOST_TIER_3 = 11
    # true
    CHANNEL_FOLLOW_ADD = 12
    # false
    GUILD_DISCOVERY_DISQUALIFIED = 14
    # false
    GUILD_DISCOVERY_REQUALIFIED = 15
    # false
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
    # false
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
    # true
    THREAD_CREATED = 18
    # true
    REPLY = 19
    # true
    CHAT_INPUT_COMMAND = 20
    # false
    THREAD_STARTER_MESSAGE = 21
    # true
    GUILD_INVITE_REMINDER = 22
    # true
    CONTEXT_MENU_COMMAND = 23
    # true*
    AUTO_MODERATION_ACTION = 24

@dataclass
class MessageActivity(Disc):
    # `type of message activity`                         
    type: int
    # party_id from a `Rich Presence event`
    party_id: str | None = field(kw_only=True, default=None)

class MessageActivityType(int, Enum):
    JOIN = 1
    SPECTATE = 2
    LISTEN = 3
    JOIN_REQUEST = 5

class MessageFlag(int, Enum):
    # this message has been published to subscribed channels (via Channel Following)
    CROSSPOSTED = 1 << 0
    # this message originated from a message in another channel (via Channel Following)
    IS_CROSSPOST = 1 << 1
    # do not include any embeds when serializing this message
    SUPPRESS_EMBEDS = 1 << 2
    # the source message for this crosspost has been deleted (via Channel Following)
    SOURCE_MESSAGE_DELETED = 1 << 3
    # this message came from the urgent message system
    URGENT = 1 << 4
    # this message has an associated thread, with the same id as the message
    HAS_THREAD = 1 << 5
    # this message is only visible to the user who invoked the Interaction
    EPHEMERAL = 1 << 6
    # this message is an Interaction Response and the bot is "thinking"
    LOADING = 1 << 7
    # this message failed to mention some roles and add their members to the thread
    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD = 1 << 8

@dataclass
class MessageReference(Disc):
    # id of the originating message                                                                                                          
    message_id: Snowflake | None = field(kw_only=True, default=None)
    # id of the originating message's channel                                                                                                
    channel_id: Snowflake | None = field(kw_only=True, default=None)
    # id of the originating message's guild                                                                                                  
    guild_id: Snowflake | None = field(kw_only=True, default=None)
    # when sending, whether to error if the referenced message doesn't exist instead of sending as a normal (non-reply) message, default true
    fail_if_not_exists: bool | None = field(kw_only=True, default=None)

@dataclass
class FollowedChannel(Disc):
    # source channel id        
    channel_id: Snowflake
    # created target webhook id
    webhook_id: Snowflake

@dataclass
class Reaction(Disc):
    # times this emoji has been used to react          
    count: int
    # whether the current user reacted using this emoji
    me: bool
    # emoji information                                
    emoji: Emoji

@dataclass
class Overwrite(Disc):
    # role or user id              
    id: Snowflake
    # either 0 (role) or 1 (member)
    type: int
    # permission bit set           
    allow: str
    # permission bit set           
    deny: str

@dataclass
class ThreadMetadata(Disc):
    # whether the thread is archived                                                                                                            
    archived: bool
    # the thread will stop showing in the channel list after `auto_archive_duration` minutes of inactivity, can be set to: 60, 1440, 4320, 10080
    auto_archive_duration: int
    # timestamp when the thread's archive status was last changed, used for calculating recent activity                                         
    archive_timestamp: str
    # whether the thread is locked; when a thread is locked, only users with MANAGE_THREADS can unarchive it                                    
    locked: bool
    # whether non-moderators can add other non-moderators to a thread; only available on private threads                                        
    invitable: bool | None = field(kw_only=True, default=None)
    # timestamp when the thread was created; only populated for threads created after 2022-01-09                                                
    create_timestamp: str | None = field(kw_only=True, default=None)

@dataclass
class ThreadMember(Disc):
    # the id of the thread                                           
    id: Snowflake | None = field(kw_only=True, default=None)
    # the id of the user                                             
    user_id: Snowflake | None = field(kw_only=True, default=None)
    # the time the current user last joined the thread               
    join_timestamp: str
    # any user-thread settings, currently only used for notifications
    flags: int

@dataclass
class DefaultReaction(Disc):
    # the id of a guild's custom emoji  
    emoji_id: Snowflake | None
    # the unicode character of the emoji
    emoji_name: str | None

@dataclass
class ForumTag(Disc):
    # the id of the tag                                                                                             
    id: Snowflake
    # the name of the tag (0-20 characters)                                                                         
    name: str
    # whether this tag can only be added to or removed from threads by a member with the `MANAGE_THREADS` permission
    moderated: bool
    # the id of a guild's custom emoji \*                                                                           
    emoji_id: Snowflake
    # the unicode character of the emoji \*                                                                         
    emoji_name: str | None

@dataclass
class Embed(Disc):
    # title of embed                                                                                             
    title: str | None = field(kw_only=True, default=None)
    # `type of embed`
    type: str | None = field(kw_only=True, default=None)
    # description of embed                                                                                       
    description: str | None = field(kw_only=True, default=None)
    # url of embed                                                                                               
    url: str | None = field(kw_only=True, default=None)
    # timestamp of embed content                                                                                 
    timestamp: str | None = field(kw_only=True, default=None)
    # color code of the embed                                                                                    
    color: int | None = field(kw_only=True, default=None)
    # footer information                                                                                         
    footer: EmbedFooter | None = field(kw_only=True, default=None)
    # image information                                                                                          
    image: EmbedImage | None = field(kw_only=True, default=None)
    # thumbnail information                                                                                      
    thumbnail: EmbedThumbnail | None = field(kw_only=True, default=None)
    # video information                                                                                          
    video: EmbedVideo | None = field(kw_only=True, default=None)
    # provider information                                                                                       
    provider: EmbedProvider | None = field(kw_only=True, default=None)
    # author information                                                                                         
    author: EmbedAuthor | None = field(kw_only=True, default=None)
    # fields information                                                                                         
    fields: list[EmbedField] | None = field(kw_only=True, default=None)

@dataclass
class EmbedThumbnail(Disc):
    # source url of thumbnail (only supports http(s) and attachments)
    url: str
    # a proxied url of the thumbnail                                 
    proxy_url: str | None = field(kw_only=True, default=None)
    # height of thumbnail                                            
    height: int | None = field(kw_only=True, default=None)
    # width of thumbnail                                             
    width: int | None = field(kw_only=True, default=None)

@dataclass
class EmbedVideo(Disc):
    # source url of video       
    url: str | None = field(kw_only=True, default=None)
    # a proxied url of the video
    proxy_url: str | None = field(kw_only=True, default=None)
    # height of video           
    height: int | None = field(kw_only=True, default=None)
    # width of video            
    width: int | None = field(kw_only=True, default=None)

@dataclass
class EmbedImage(Disc):
    # source url of image (only supports http(s) and attachments)
    url: str
    # a proxied url of the image                                 
    proxy_url: str | None = field(kw_only=True, default=None)
    # height of image                                            
    height: int | None = field(kw_only=True, default=None)
    # width of image                                             
    width: int | None = field(kw_only=True, default=None)

@dataclass
class EmbedProvider(Disc):
    # name of provider
    name: str | None = field(kw_only=True, default=None)
    # url of provider 
    url: str | None = field(kw_only=True, default=None)

@dataclass
class EmbedAuthor(Disc):
    # name of author                                            
    name: str
    # url of author                                             
    url: str | None = field(kw_only=True, default=None)
    # url of author icon (only supports http(s) and attachments)
    icon_url: str | None = field(kw_only=True, default=None)
    # a proxied url of author icon                              
    proxy_icon_url: str | None = field(kw_only=True, default=None)

@dataclass
class EmbedFooter(Disc):
    # footer text                                               
    text: str
    # url of footer icon (only supports http(s) and attachments)
    icon_url: str | None = field(kw_only=True, default=None)
    # a proxied url of footer icon                              
    proxy_icon_url: str | None = field(kw_only=True, default=None)

@dataclass
class EmbedField(Disc):
    # name of the field                              
    name: str
    # value of the field                             
    value: str
    # whether or not this field should display inline
    inline: bool | None = field(kw_only=True, default=None)

@dataclass
class Attachment(Disc):
    # attachment id                                                          
    id: Snowflake
    # name of file attached                                                  
    filename: str
    # description for the file (max 1024 characters)                         
    description: str | None = field(kw_only=True, default=None)
    # the attachment's `media type`
    content_type: str | None = field(kw_only=True, default=None)
    # size of file in bytes                                                  
    size: int
    # source url of file                                                     
    url: str
    # a proxied url of file                                                  
    proxy_url: str
    # height of file (if image)                                              
    height: int | None = field(kw_only=True, default=None)
    # width of file (if image)                                               
    width: int | None = field(kw_only=True, default=None)
    # whether this attachment is ephemeral                                   
    ephemeral: bool | None = field(kw_only=True, default=None)

@dataclass
class ChannelMention(Disc):
    # id of the channel                                                          
    id: Snowflake
    # id of the guild containing the channel                                     
    guild_id: Snowflake
    # the `type of channel`
    type: int
    # the name of the channel                                                    
    name: str

class AllowedMentionType(str, Enum):
    # Controls role mentions
    ROLES = "roles"
    # Controls user mentions
    USERS = "users"
    # Controls @everyone and @here mentions
    EVERYONE = "everyone"

@dataclass
class AllowedMentions(Disc):
    # An array of `allowed mention types` to parse from the content.
    parse: list[AllowedMentionType]
    # Array of role_ids to mention (Max size of 100)                                                                                       
    roles: list[Snowflake]
    # Array of user_ids to mention (Max size of 100)                                                                                       
    users: list[Snowflake]
    # For replies, whether to mention the author of the message being replied to (default false)                                           
    replied_user: bool

@dataclass
class ForumThreadMessageParams(Disc):
    # Message contents (up to 2000 characters)                                                                                                                                   
    content: str | None = field(kw_only=True, default=None)
    # Embedded `rich` content (up to 6000 characters)                                                                                                                            
    embeds: list[Embed] | None = field(kw_only=True, default=None)
    # Allowed mentions for the message                                                                                                                                           
    allowed_mentions: AllowedMentions | None = field(kw_only=True, default=None)
    # Components to include with the message                                                                                                                                     
    components: list[MessageComponent] | None = field(kw_only=True, default=None)
    # IDs of up to 3 `stickers` in the server to send in the message                                                                     
    sticker_ids: list[Snowflake] | None = field(kw_only=True, default=None)
    # JSON-encoded body of non-file params, only for `multipart/form-data` requests. See `Uploading Files`                                      
    payload_json: str | None = field(kw_only=True, default=None)
    # Attachment objects with `filename` and `description`. See `Uploading Files`                                                               
    attachments: list[Attachment] | None = field(kw_only=True, default=None)
    # `Message flags`
    flags: int | None = field(kw_only=True, default=None)

@dataclass
class Sticker(Disc):
    # `id of the sticker`                                                                                                               
    id: Snowflake
    # for standard stickers, id of the pack the sticker is from                                                                                                           
    pack_id: Snowflake | None = field(kw_only=True, default=None)
    # name of the sticker                                                                                                                                                 
    name: str
    # description of the sticker                                                                                                                                          
    description: str | None
    # autocomplete/suggestion tags for the sticker (max 200 characters)                                                                                                   
    tags: str
    # **Deprecated** previously the sticker asset hash, now an empty string                                                                                               
    asset: str | None = field(kw_only=True, default=None)
    # `type of sticker`                                                                                             
    type: int
    # `type of sticker format`                                                                               
    format_type: int
    # whether this guild sticker can be used, may be false due to loss of Server Boosts                                                                                   
    available: bool | None = field(kw_only=True, default=None)
    # id of the guild that owns this sticker                                                                                                                              
    guild_id: Snowflake | None = field(kw_only=True, default=None)
    # the user that uploaded the guild sticker                                                                                                                            
    user: User | None = field(kw_only=True, default=None)
    # the standard sticker's sort order within its pack                                                                                                                   
    sort_value: int | None = field(kw_only=True, default=None)

class StickerType(int, Enum):
    # an official sticker in a pack, part of Nitro or in a removed purchasable pack
    STANDARD = 1
    # a sticker uploaded to a guild for the guild's members
    GUILD = 2

class StickerFormatType(int, Enum):
    PNG = 1
    APNG = 2
    LOTTIE = 3

@dataclass
class StickerItem(Disc):
    # id of the sticker                                                                    
    id: Snowflake
    # name of the sticker                                                                  
    name: str
    # `type of sticker format`
    format_type: int

@dataclass
class StickerPack(Disc):
    # id of the sticker pack                                                   
    id: Snowflake
    # the stickers in the pack                                                 
    stickers: list[Sticker]
    # name of the sticker pack                                                 
    name: str
    # id of the pack's SKU                                                     
    sku_id: Snowflake
    # id of a sticker in the pack which is shown as the pack's icon            
    cover_sticker_id: Snowflake | None = field(kw_only=True, default=None)
    # description of the sticker pack                                          
    description: str
    # id of the sticker pack's `banner image`
    banner_asset_id: Snowflake | None = field(kw_only=True, default=None)

@dataclass
class GuildScheduledEvent(Disc):
    # the id of the scheduled event                                                                                                                                                                                        
    id: Snowflake
    # the guild id which the scheduled event belongs to                                                                                                                                                                    
    guild_id: Snowflake
    # the channel id in which the scheduled event will be hosted, or `null` if `scheduled entity type` is `EXTERNAL`
    channel_id: Snowflake | None
    # the id of the user that created the scheduled event *                                                                                                                                                                
    creator_id: Snowflake | None = field(kw_only=True, default=None)
    # the name of the scheduled event (1-100 characters)                                                                                                                                                                   
    name: str
    # the description of the scheduled event (1-1000 characters)                                                                                                                                                           
    description: str | None = field(kw_only=True, default=None)
    # the time the scheduled event will start                                                                                                                                                                              
    scheduled_start_time: str
    # the time the scheduled event will end, required if entity_type is `EXTERNAL`                                                                                                                                         
    scheduled_end_time: str | None
    # the privacy level of the scheduled event                                                                                                                                                                             
    privacy_level: GuildScheduledEventPrivacyLevel
    # the status of the scheduled event                                                                                                                                                                                    
    status: GuildScheduledEventStatusType
    # the type of the scheduled event                                                                                                                                                                                      
    entity_type: GuildScheduledEventEntityType
    # the id of an entity associated with a guild scheduled event                                                                                                                                                          
    entity_id: Snowflake | None
    # additional metadata for the guild scheduled event                                                                                                                                                                    
    entity_metadata: GuildScheduledEventEntityMetadata | None
    # the user that created the scheduled event                                                                                                                                                                            
    creator: User | None = field(kw_only=True, default=None)
    # the number of users subscribed to the scheduled event                                                                                                                                                                
    user_count: int | None = field(kw_only=True, default=None)
    # the `cover image hash` of the scheduled event                                                                                                                                      
    image: str | None = field(kw_only=True, default=None)

class GuildScheduledEventPrivacyLevel(int, Enum):
    # the scheduled event is only accessible to guild members
    GUILD_ONLY = 2

class GuildScheduledEventEntityType(int, Enum):
    STAGE_INSTANCE = 1
    VOICE = 2
    EXTERNAL = 3

class GuildScheduledEventStatusType(int, Enum):
    SCHEDULED = 1
    ACTIVE = 2
    COMPLETED = 3
    CANCELED = 4

@dataclass
class GuildScheduledEventEntityMetadata(Disc):
    # location of the event (1-100 characters)
    location: str | None = field(kw_only=True, default=None)

@dataclass
class GuildScheduledEventUser(Disc):
    # the scheduled event id which the user subscribed to                                                
    guild_scheduled_event_id: Snowflake
    # user which subscribed to an event                                                                  
    user: User
    # guild member data for this user for the guild which this event belongs to, if any                  
    member: GuildMember | None = field(kw_only=True, default=None)

@dataclass
class Webhook(Disc):
    # the id of the webhook                                                                                        
    id: Snowflake
    # the `type` of the webhook                              
    type: int
    # the guild id this webhook is for, if any                                                                     
    guild_id: Snowflake | None = field(kw_only=True, default=None)
    # the channel id this webhook is for, if any                                                                   
    channel_id: Snowflake | None
    # the user this webhook was created by (not returned when getting a webhook with its token)                    
    user: User | None = field(kw_only=True, default=None)
    # the default name of the webhook                                                                              
    name: str | None
    # the default user avatar `hash` of the webhook                              
    avatar: str | None
    # the secure token of the webhook (returned for Incoming Webhooks)                                             
    token: str | None = field(kw_only=True, default=None)
    # the bot/OAuth2 application that created this webhook                                                         
    application_id: Snowflake | None
    # the guild of the channel that this webhook is following (returned for Channel Follower Webhooks)             
    source_guild: Guild | None = field(kw_only=True, default=None)
    # the channel that this webhook is following (returned for Channel Follower Webhooks)                          
    source_channel: Channel | None = field(kw_only=True, default=None)
    # the url used for executing the webhook (returned by the `webhooks`
    url: str | None = field(kw_only=True, default=None)

class WebhookType(int, Enum):
    # Incoming Webhooks can post messages to channels with a generated token
    INCOMING = 1
    # Channel Follower Webhooks are internal webhooks used with Channel Following to post new messages into channels
    CHANNEL_FOLLOWER = 2
    # Application webhooks are webhooks used with Interactions
    APPLICATION = 3

@dataclass
class Invite(Disc):
    # the invite code (unique ID)                                                                                                                   
    code: str
    # the guild this invite is for                                                                                                                  
    guild: Guild | None = field(kw_only=True, default=None)
    # the channel this invite is for                                                                                                                
    channel: Channel | None
    # the user who created the invite                                                                                                               
    inviter: User | None = field(kw_only=True, default=None)
    # the `type of target` for this voice channel invite                                  
    target_type: int | None = field(kw_only=True, default=None)
    # the user whose stream to display for this voice channel stream invite                                                                         
    target_user: User | None = field(kw_only=True, default=None)
    # the embedded application to open for this voice channel embedded application invite                                                           
    target_application: Application | None = field(kw_only=True, default=None)
    # approximate count of online members, returned from the `GET /invites/<code>` endpoint when `with_counts` is `true`                            
    approximate_presence_count: int | None = field(kw_only=True, default=None)
    # approximate count of total members, returned from the `GET /invites/<code>` endpoint when `with_counts` is `true`                             
    approximate_member_count: int | None = field(kw_only=True, default=None)
    # the expiration date of this invite, returned from the `GET /invites/<code>` endpoint when `with_expiration` is `true`                         
    expires_at: str | None = field(kw_only=True, default=None)
    # stage instance data if there is a `public Stage instance`
    stage_instance: InviteStageInstance | None = field(kw_only=True, default=None)
    # guild scheduled event data, only included if `guild_scheduled_event_id` contains a valid guild scheduled event id                             
    guild_scheduled_event: GuildScheduledEvent | None = field(kw_only=True, default=None)

class InviteTargetType(int, Enum):
    STREAM = 1
    EMBEDDED_APPLICATION = 2

@dataclass
class InviteMetadata(Disc):
    # number of times this invite has been used           
    uses: int
    # max number of times this invite can be used         
    max_uses: int
    # duration (in seconds) after which the invite expires
    max_age: int
    # whether this invite only grants temporary membership
    temporary: bool
    # when this invite was created                        
    created_at: str

@dataclass
class InviteStageInstance(Disc):
    # the members speaking in the Stage                 
    members: list[GuildMember]
    # the number of users in the Stage                  
    participant_count: int
    # the number of users speaking in the Stage         
    speaker_count: int
    # the topic of the Stage instance (1-120 characters)
    topic: str

@dataclass
class Application(Disc):
    # the id of the app                                                                                                        
    id: Snowflake
    # the name of the app                                                                                                      
    name: str
    # the `icon hash` of the app                                                             
    icon: str | None
    # the description of the app                                                                                               
    description: str
    # an array of rpc origin urls, if rpc is enabled                                                                           
    rpc_origins: list[str] | None = field(kw_only=True, default=None)
    # when false only app owner can join the app's bot to guilds                                                               
    bot_public: bool
    # when true the app's bot will only join upon completion of the full oauth2 code grant flow                                
    bot_require_code_grant: bool
    # the url of the app's terms of service                                                                                    
    terms_of_service_url: str | None = field(kw_only=True, default=None)
    # the url of the app's privacy policy                                                                                      
    privacy_policy_url: str | None = field(kw_only=True, default=None)
    # partial user object containing info on the owner of the application                                                      
    owner: User | None = field(kw_only=True, default=None)
    # the hex encoded key for verification in interactions and the GameSDK's `GetTicket`
    verify_key: str
    # if the application belongs to a team, this will be a list of the members of that team                                    
    team: Team | None
    # if this application is a game sold on Discord, this field will be the guild to which it has been linked                  
    guild_id: Snowflake | None = field(kw_only=True, default=None)
    # if this application is a game sold on Discord, this field will be the id of the "Game SKU" that is created, if exists    
    primary_sku_id: Snowflake | None = field(kw_only=True, default=None)
    # if this application is a game sold on Discord, this field will be the URL slug that links to the store page              
    slug: str | None = field(kw_only=True, default=None)
    # the application's default rich presence invite `cover image hash`                      
    cover_image: str | None = field(kw_only=True, default=None)
    # the application's public `flags`                       
    flags: int | None = field(kw_only=True, default=None)
    # up to 5 tags describing the content and functionality of the application                                                 
    tags: list[str] | None = field(kw_only=True, default=None)
    # settings for the application's default in-app authorization link, if enabled                                             
    install_params: InstallParams | None = field(kw_only=True, default=None)
    # the application's default custom authorization link, if enabled                                                          
    custom_install_url: str | None = field(kw_only=True, default=None)

class ApplicationFlag(int, Enum):
    # Intent required for bots in **100 or more servers** to receive ``presence_update` events`
    GATEWAY_PRESENCE = 1 << 12
    # Intent required for bots in under 100 servers to receive ``presence_update` events`, found in Bot Settings
    GATEWAY_PRESENCE_LIMITED = 1 << 13
    # Intent required for bots in **100 or more servers** to receive member-related events like `guild_member_add`. See list of member-related events `under `GUILD_MEMBERS``
    GATEWAY_GUILD_MEMBERS = 1 << 14
    # Intent required for bots in under 100 servers to receive member-related events like `guild_member_add`, found in Bot Settings. See list of member-related events `under `GUILD_MEMBERS``
    GATEWAY_GUILD_MEMBERS_LIMITED = 1 << 15
    # Indicates unusual growth of an app that prevents verification
    VERIFICATION_PENDING_GUILD_LIMIT = 1 << 16
    # Indicates if an app is embedded within the Discord client (currently unavailable publicly)
    EMBEDDED = 1 << 17
    # Intent required for bots in **100 or more servers** to receive `message content`
    GATEWAY_MESSAGE_CONTENT = 1 << 18
    # Intent required for bots in under 100 servers to receive `message content`, found in Bot Settings
    GATEWAY_MESSAGE_CONTENT_LIMITED = 1 << 19
    # Indicates if an app has registered global `application commands`
    APPLICATION_COMMAND_BADGE = 1 << 23

@dataclass
class InstallParams(Disc):
    # the `scopes` to add the application to the server with
    scopes: list[str]
    # the `permissions` to request for the bot role                                   
    permissions: str

@dataclass
class User(Disc):
    # the user's id                                                                                       
    id: Snowflake
    # the user's username, not unique across the platform                                                 
    username: str
    # the user's 4-digit discord-tag                                                                      
    discriminator: str
    # the user's `avatar hash`                                          
    avatar: str | None
    # whether the user belongs to an OAuth2 application                                                   
    bot: bool | None = field(kw_only=True, default=None)
    # whether the user is an Official Discord System user (part of the urgent message system)             
    system: bool | None = field(kw_only=True, default=None)
    # whether the user has two factor enabled on their account                                            
    mfa_enabled: bool | None = field(kw_only=True, default=None)
    # the user's `banner hash`                                          
    banner: str | None = field(kw_only=True, default=None)
    # the user's banner color encoded as an integer representation of hexadecimal color code              
    accent_color: int | None = field(kw_only=True, default=None)
    # the user's chosen `language option`                                        
    locale: str | None = field(kw_only=True, default=None)
    # whether the email on this account has been verified                                                 
    verified: bool | None = field(kw_only=True, default=None)
    # the user's email                                                                                    
    email: str | None = field(kw_only=True, default=None)
    # the `flags` on a user's account                        
    flags: int | None = field(kw_only=True, default=None)
    # the `type of Nitro subscription` on a user's account
    premium_type: int | None = field(kw_only=True, default=None)
    # the public `flags` on a user's account                 
    public_flags: int | None = field(kw_only=True, default=None)

class UserFlag(int, Enum):
    # Discord Employee
    STAFF = 1 << 0
    # Partnered Server Owner
    PARTNER = 1 << 1
    # HypeSquad Events Member
    HYPESQUAD = 1 << 2
    # Bug Hunter Level 1
    BUG_HUNTER_LEVEL_1 = 1 << 3
    # House Bravery Member
    HYPESQUAD_ONLINE_HOUSE_1 = 1 << 6
    # House Brilliance Member
    HYPESQUAD_ONLINE_HOUSE_2 = 1 << 7
    # House Balance Member
    HYPESQUAD_ONLINE_HOUSE_3 = 1 << 8
    # Early Nitro Supporter
    PREMIUM_EARLY_SUPPORTER = 1 << 9
    # User is a `team`
    TEAM_PSEUDO_USER = 1 << 10
    # Bug Hunter Level 2
    BUG_HUNTER_LEVEL_2 = 1 << 14
    # Verified Bot
    VERIFIED_BOT = 1 << 16
    # Early Verified Bot Developer
    VERIFIED_DEVELOPER = 1 << 17
    # Discord Certified Moderator
    CERTIFIED_MODERATOR = 1 << 18
    # Bot uses only `HTTP interactions` and is shown in the online member list
    BOT_HTTP_INTERACTIONS = 1 << 19

class PremiumType(int, Enum):
    NONE = 0
    NITROCLASSIC = 1
    NITRO = 2

@dataclass
class Connection(Disc):
    # id of the connection account                                                            
    id: str
    # the username of the connection account                                                  
    name: str
    # the `service` of this connection       
    type: str
    # whether the connection is revoked                                                       
    revoked: bool | None = field(kw_only=True, default=None)
    # an array of partial `server integrations`     
    integrations: list[Integration] | None = field(kw_only=True, default=None)
    # whether the connection is verified                                                      
    verified: bool
    # whether friend sync is enabled for this connection                                      
    friend_sync: bool
    # whether activities related to this connection will be shown in presence updates         
    show_activity: bool
    # whether this connection has a corresponding third party OAuth2 token                    
    two_way_link: bool
    # `visibility` of this connection
    visibility: int

class VisibilityType(int, Enum):
    # invisible to everyone except the user themselves
    NONE = 0
    # visible to everyone
    EVERYONE = 1

@dataclass
class AuditLog(Disc):
    # List of application commands referenced in the audit log   
    application_commands: list[ApplicationCommand]
    # List of audit log entries, sorted from most to least recent
    audit_log_entries: list[AuditLogEntry]
    # List of auto moderation rules referenced in the audit log  
    auto_moderation_rules: list[AutoModerationRule]
    # List of guild scheduled events referenced in the audit log 
    guild_scheduled_events: list[GuildScheduledEvent]
    # List of partial integration objects                        
    integrations: list[Integration]
    # List of threads referenced in the audit log\*              
    threads: list[Channel]
    # List of users referenced in the audit log                  
    users: list[User]
    # List of webhooks referenced in the audit log               
    webhooks: list[Webhook]

@dataclass
class AuditLogEntry(Disc):
    # ID of the affected entity (webhook, user, role, etc.)
    target_id: str | None
    # Changes made to the target_id                        
    changes: list[AuditLogChange] | None = field(kw_only=True, default=None)
    # User or app that made the changes                    
    user_id: Snowflake | None
    # ID of the entry                                      
    id: Snowflake
    # Type of action that occurred                         
    action_type: AuditLogEventType
    # Additional info for certain event types              
    options: OptionalAuditEntryInfo | None = field(kw_only=True, default=None)
    # Reason for the change (1-512 characters)             
    reason: str | None = field(kw_only=True, default=None)

class AuditLogEventType(int, Enum):
    # Server settings were updated                              | `Guild`
    GUILD_UPDATE = 1
    # Channel was created                                       | `Channel`
    CHANNEL_CREATE = 10
    # Channel settings were updated                             | `Channel`
    CHANNEL_UPDATE = 11
    # Channel was deleted                                       | `Channel`
    CHANNEL_DELETE = 12
    # Permission overwrite was added to a channel               | `Channel Overwrite`
    CHANNEL_OVERWRITE_CREATE = 13
    # Permission overwrite was updated for a channel            | `Channel Overwrite`
    CHANNEL_OVERWRITE_UPDATE = 14
    # Permission overwrite was deleted from a channel           | `Channel Overwrite`
    CHANNEL_OVERWRITE_DELETE = 15
    # Member was removed from server                            |
    MEMBER_KICK = 20
    # Members were pruned from server                           |
    MEMBER_PRUNE = 21
    # Member was banned from server                             |
    MEMBER_BAN_ADD = 22
    # Server ban was lifted for a member                        |
    MEMBER_BAN_REMOVE = 23
    # Member was updated in server                              | `Member`
    MEMBER_UPDATE = 24
    # Member was added or removed from a role                   | `Partial Role`\*
    MEMBER_ROLE_UPDATE = 25
    # Member was moved to a different voice channel             |
    MEMBER_MOVE = 26
    # Member was disconnected from a voice channel              |
    MEMBER_DISCONNECT = 27
    # Bot user was added to server                              |
    BOT_ADD = 28
    # Role was created                                          | `Role`
    ROLE_CREATE = 30
    # Role was edited                                           | `Role`
    ROLE_UPDATE = 31
    # Role was deleted                                          | `Role`
    ROLE_DELETE = 32
    # Server invite was created                                 | `Invite`*
    INVITE_CREATE = 40
    # Server invite was updated                                 | `Invite`*
    INVITE_UPDATE = 41
    # Server invite was deleted                                 | `Invite`*
    INVITE_DELETE = 42
    # Webhook was created                                       | `Webhook`\*
    WEBHOOK_CREATE = 50
    # Webhook properties or channel were updated                | `Webhook`\*
    WEBHOOK_UPDATE = 51
    # Webhook was deleted                                       | `Webhook`\*
    WEBHOOK_DELETE = 52
    # Emoji was created                                         | `Emoji`
    EMOJI_CREATE = 60
    # Emoji name was updated                                    | `Emoji`
    EMOJI_UPDATE = 61
    # Emoji was deleted                                         | `Emoji`
    EMOJI_DELETE = 62
    # Single message was deleted                                |
    MESSAGE_DELETE = 72
    # Multiple messages were deleted                            |
    MESSAGE_BULK_DELETE = 73
    # Message was pinned to a channel                           |
    MESSAGE_PIN = 74
    # Message was unpinned from a channel                       |
    MESSAGE_UNPIN = 75
    # App was added to server                                   | `Integration`
    INTEGRATION_CREATE = 80
    # App was updated (as an example, its scopes were updated)  | `Integration`
    INTEGRATION_UPDATE = 81
    # App was removed from server                               | `Integration`
    INTEGRATION_DELETE = 82
    # Stage instance was created (stage channel becomes live)   | `Stage Instance`
    STAGE_INSTANCE_CREATE = 83
    # Stage instance details were updated                       | `Stage Instance`
    STAGE_INSTANCE_UPDATE = 84
    # Stage instance was deleted (stage channel no longer live) | `Stage Instance`
    STAGE_INSTANCE_DELETE = 85
    # Sticker was created                                       | `Sticker`
    STICKER_CREATE = 90
    # Sticker details were updated                              | `Sticker`
    STICKER_UPDATE = 91
    # Sticker was deleted                                       | `Sticker`
    STICKER_DELETE = 92
    # Event was created                                         | `Guild Scheduled Event`
    GUILD_SCHEDULED_EVENT_CREATE = 100
    # Event was updated                                         | `Guild Scheduled Event`
    GUILD_SCHEDULED_EVENT_UPDATE = 101
    # Event was cancelled                                       | `Guild Scheduled Event`
    GUILD_SCHEDULED_EVENT_DELETE = 102
    # Thread was created in a channel                           | `Thread`
    THREAD_CREATE = 110
    # Thread was updated                                        | `Thread`
    THREAD_UPDATE = 111
    # Thread was deleted                                        | `Thread`
    THREAD_DELETE = 112
    # Permissions were updated for a command                    | `Command Permission`\*
    APPLICATION_COMMAND_PERMISSION_UPDATE = 121
    # Auto Moderation rule was created                          | `Auto Moderation Rule`
    AUTO_MODERATION_RULE_CREATE = 140
    # Auto Moderation rule was updated                          | `Auto Moderation Rule`
    AUTO_MODERATION_RULE_UPDATE = 141
    # Auto Moderation rule was deleted                          | `Auto Moderation Rule`
    AUTO_MODERATION_RULE_DELETE = 142
    # Message was blocked by AutoMod                            |
    AUTO_MODERATION_BLOCK_MESSAGE = 143
    # Message was flagged by AutoMod                            |
    AUTO_MODERATION_FLAG_TO_CHANNEL = 144
    # Member was timed out by AutoMod                           |
    AUTO_MODERATION_USER_COMMUNICATION_DISABLED = 145

@dataclass
class OptionalAuditEntryInfo(Disc):
    # ID of the app whose permissions were targeted                   
    application_id: Snowflake
    # Name of the Auto Moderation rule that was triggered             
    auto_moderation_rule_name: str
    # Trigger type of the Auto Moderation rule that was triggered     
    auto_moderation_rule_trigger_type: str
    # Channel in which the entities were targeted                     
    channel_id: Snowflake
    # Number of entities that were targeted                           
    count: str
    # Number of days after which inactive members were kicked         
    delete_member_days: str
    # ID of the overwritten entity                                    
    id: Snowflake
    # Number of members removed by the prune                          
    members_removed: str
    # ID of the message that was targeted                             
    message_id: Snowflake
    # Name of the role if type is `"0"` (not present if type is `"1"`)
    role_name: str
    # Type of overwritten entity - role (`"0"`) or member (`"1"`)     
    type: str

@dataclass
class AuditLogChange(Disc):
    # New value of the key                                                                                                              
    new_value: Any | None = field(kw_only=True, default=None)
    # Old value of the key                                                                                                              
    old_value: Any | None = field(kw_only=True, default=None)
    # Name of the changed entity, with a few `exceptions`
    key: str

@dataclass
class VoiceState(Disc):
    # the guild id this voice state is for             
    guild_id: Snowflake | None = field(kw_only=True, default=None)
    # the channel id this user is connected to         
    channel_id: Snowflake | None
    # the user id this voice state is for              
    user_id: Snowflake
    # the guild member this voice state is for         
    member: GuildMember | None = field(kw_only=True, default=None)
    # the session id for this voice state              
    session_id: str
    # whether this user is deafened by the server      
    deaf: bool
    # whether this user is muted by the server         
    mute: bool
    # whether this user is locally deafened            
    self_deaf: bool
    # whether this user is locally muted               
    self_mute: bool
    # whether this user is streaming using "Go Live"   
    self_stream: bool | None = field(kw_only=True, default=None)
    # whether this user's camera is enabled            
    self_video: bool
    # whether this user's permission to speak is denied
    suppress: bool
    # the time at which the user requested to speak    
    request_to_speak_timestamp: str | None

@dataclass
class VoiceRegion(Disc):
    # unique ID for the region                                             
    id: str
    # name of the region                                                   
    name: str
    # true for a single server that is closest to the current user's client
    optimal: bool
    # whether this is a deprecated voice region (avoid switching to these) 
    deprecated: bool
    # whether this is a custom voice region (used for events/etc)          
    custom: bool

@dataclass
class Guild(Disc):
    # guild id                                                                                                                                                              
    id: Snowflake
    # guild name (2-100 characters, excluding trailing and leading whitespace)                                                                                              
    name: str
    # `icon hash`                                                                                                                         
    icon: str | None
    # `icon hash`, returned when in the template object                                                                                   
    icon_hash: str | None = field(kw_only=True, default=None)
    # `splash hash`                                                                                                                       
    splash: str | None
    # `discovery splash hash`; only present for guilds with the "DISCOVERABLE" feature                                                    
    discovery_splash: str | None
    # true if `the user` is the owner of the guild                                                                            
    owner: bool | None = field(kw_only=True, default=None)
    # id of owner                                                                                                                                                           
    owner_id: Snowflake
    # total permissions for `the user`                                                     
    permissions: str | None = field(kw_only=True, default=None)
    # `voice region`                                                                               
    region: str | None = field(kw_only=True, default=None)
    # id of afk channel                                                                                                                                                     
    afk_channel_id: Snowflake | None
    # afk timeout in seconds, can be set to: 60, 300, 900, 1800, 3600                                                                                                       
    afk_timeout: int
    # true if the server widget is enabled                                                                                                                                  
    widget_enabled: bool | None = field(kw_only=True, default=None)
    # the channel id that the widget will generate an invite to, or `null` if set to no invite                                                                              
    widget_channel_id: Snowflake | None = field(kw_only=True, default=None)
    # `verification level` required for the guild                                                                    
    verification_level: int
    # default `message notifications level`                                                          
    default_message_notifications: int
    # `explicit content filter level`                                                                     
    explicit_content_filter: int
    # roles in the guild                                                                                                                                                    
    roles: list[Role]
    # custom guild emojis                                                                                                                                                   
    emojis: list[Emoji]
    # enabled guild features                                                                                                                                                
    features: list[GuildFeature]
    # required `MFA level` for the guild                                                                                      
    mfa_level: int
    # application id of the guild creator if it is bot-created                                                                                                              
    application_id: Snowflake | None
    # the id of the channel where guild notices such as welcome messages and boost events are posted                                                                        
    system_channel_id: Snowflake | None
    # `system channel flags`                                                                                       
    system_channel_flags: int
    # the id of the channel where Community guilds can display rules and/or guidelines                                                                                      
    rules_channel_id: Snowflake | None
    # the maximum number of presences for the guild (`null` is always returned, apart from the largest of guilds)                                                           
    max_presences: int | None = field(kw_only=True, default=None)
    # the maximum number of members for the guild                                                                                                                           
    max_members: int | None = field(kw_only=True, default=None)
    # the vanity url code for the guild                                                                                                                                     
    vanity_url_code: str | None
    # the description of a guild                                                                                                                                            
    description: str | None
    # `banner hash`                                                                                                                       
    banner: str | None
    # `premium tier`                                                                                  
    premium_tier: int
    # the number of boosts this guild currently has                                                                                                                         
    premium_subscription_count: int | None = field(kw_only=True, default=None)
    # the preferred `locale` of a Community guild; used in server discovery and notices from Discord, and sent in interactions; defaults to "en-US"
    preferred_locale: str
    # the id of the channel where admins and moderators of Community guilds receive notices from Discord                                                                    
    public_updates_channel_id: Snowflake | None
    # the maximum amount of users in a video channel                                                                                                                        
    max_video_channel_users: int | None = field(kw_only=True, default=None)
    # approximate number of members in this guild, returned from the `GET /guilds/<id>` endpoint when `with_counts` is `true`                                               
    approximate_member_count: int | None = field(kw_only=True, default=None)
    # approximate number of non-offline members in this guild, returned from the `GET /guilds/<id>` endpoint when `with_counts` is `true`                                   
    approximate_presence_count: int | None = field(kw_only=True, default=None)
    # the welcome screen of a Community guild, shown to new members, returned in an `Invite`'s guild object                           
    welcome_screen: WelcomeScreen | None = field(kw_only=True, default=None)
    # `guild NSFW level`                                                                                               
    nsfw_level: int
    # custom guild stickers                                                                                                                                                 
    stickers: list[Sticker] | None = field(kw_only=True, default=None)
    # whether the guild has the boost progress bar enabled                                                                                                                  
    premium_progress_bar_enabled: bool

class DefaultMessageNotificationLevel(int, Enum):
    # members will receive notifications for all messages by default
    ALL_MESSAGES = 0
    # members will receive notifications only for messages that @mention them by default
    ONLY_MENTIONS = 1

class ExplicitContentFilterLevel(int, Enum):
    # media content will not be scanned
    DISABLED = 0
    # media content sent by members without roles will be scanned
    MEMBERS_WITHOUT_ROLES = 1
    # media content sent by all members will be scanned
    ALL_MEMBERS = 2

class MFALevel(int, Enum):
    # guild has no MFA/2FA requirement for moderation actions
    NONE = 0
    # guild has a 2FA requirement for moderation actions
    ELEVATED = 1

class VerificationLevel(int, Enum):
    # unrestricted
    NONE = 0
    # must have verified email on account
    LOW = 1
    # must be registered on Discord for longer than 5 minutes
    MEDIUM = 2
    # must be a member of the server for longer than 10 minutes
    HIGH = 3
    # must have a verified phone number
    VERY_HIGH = 4

class GuildNSFWLevel(int, Enum):
    DEFAULT = 0
    EXPLICIT = 1
    SAFE = 2
    AGE_RESTRICTED = 3

class SystemChannelFlag(int, Enum):
    # Suppress member join notifications
    SUPPRESS_JOIN_NOTIFICATIONS = 1 << 0
    # Suppress server boost notifications
    SUPPRESS_PREMIUM_SUBSCRIPTIONS = 1 << 1
    # Suppress server setup tips
    SUPPRESS_GUILD_REMINDER_NOTIFICATIONS = 1 << 2
    # Hide member join sticker reply buttons
    SUPPRESS_JOIN_NOTIFICATION_REPLIES = 1 << 3

class GuildFeature(str, Enum):
    # guild has access to set an animated guild banner image
    ANIMATED_BANNER = "ANIMATED_BANNER"
    # guild has access to set an animated guild icon
    ANIMATED_ICON = "ANIMATED_ICON"
    # guild has set up auto moderation rules
    AUTO_MODERATION = "AUTO_MODERATION"
    # guild has access to set a guild banner image
    BANNER = "BANNER"
    # guild can enable welcome screen, Membership Screening, stage channels and discovery, and receives community updates
    COMMUNITY = "COMMUNITY"
    # guild is able to be discovered in the directory
    DISCOVERABLE = "DISCOVERABLE"
    # guild is able to be featured in the directory
    FEATURABLE = "FEATURABLE"
    # guild has paused invites, preventing new users from joining
    INVITES_DISABLED = "INVITES_DISABLED"
    # guild has access to set an invite splash background
    INVITE_SPLASH = "INVITE_SPLASH"
    # guild has enabled `Membership Screening`
    MEMBER_VERIFICATION_GATE_ENABLED = "MEMBER_VERIFICATION_GATE_ENABLED"
    # guild has enabled monetization
    MONETIZATION_ENABLED = "MONETIZATION_ENABLED"
    # guild has increased custom sticker slots
    MORE_STICKERS = "MORE_STICKERS"
    # guild has access to create announcement channels
    NEWS = "NEWS"
    # guild is partnered
    PARTNERED = "PARTNERED"
    # guild can be previewed before joining via Membership Screening or the directory
    PREVIEW_ENABLED = "PREVIEW_ENABLED"
    # guild has access to create private threads
    PRIVATE_THREADS = "PRIVATE_THREADS"
    # guild is able to set role icons
    ROLE_ICONS = "ROLE_ICONS"
    # guild has enabled ticketed events
    TICKETED_EVENTS_ENABLED = "TICKETED_EVENTS_ENABLED"
    # guild has access to set a vanity URL
    VANITY_URL = "VANITY_URL"
    # guild is verified
    VERIFIED = "VERIFIED"
    # guild has access to set 384kbps bitrate in voice (previously VIP voice servers)
    VIP_REGIONS = "VIP_REGIONS"
    # guild has enabled the welcome screen
    WELCOME_SCREEN_ENABLED = "WELCOME_SCREEN_ENABLED"

class MutableGuildFeature(str, Enum):
    # Enables Community Features in the guild
    COMMUNITY = "COMMUNITY"
    # Pauses all invites/access to the server
    INVITES_DISABLED = "INVITES_DISABLED"
    # Enables discovery in the guild, making it publicly listed
    DISCOVERABLE = "DISCOVERABLE"

@dataclass
class GuildPreview(Disc):
    # guild id                                                   
    id: Snowflake
    # guild name (2-100 characters)                              
    name: str
    # `icon hash`              
    icon: str | None
    # `splash hash`            
    splash: str | None
    # `discovery splash hash`  
    discovery_splash: str | None
    # custom guild emojis                                        
    emojis: list[Emoji]
    # enabled guild features                                     
    features: list[GuildFeature]
    # approximate number of members in this guild                
    approximate_member_count: int
    # approximate number of online members in this guild         
    approximate_presence_count: int
    # the description for the guild                              
    description: str | None
    # custom guild stickers                                     
    stickers: list[Sticker]

@dataclass
class GuildWidgetSettings(Disc):
    # whether the widget is enabled
    enabled: bool
    # the widget channel id        
    channel_id: Snowflake | None

@dataclass
class GuildWidget(Disc):
    # guild id                                                            
    id: Snowflake
    # guild name (2-100 characters)                                       
    name: str
    # instant invite for the guilds specified widget invite channel       
    instant_invite: str | None
    # voice and stage channels which are accessible by @everyone          
    channels: list[Channel]
    # special widget user objects that includes users presence (Limit 100)
    members: list[User]
    # number of online members in this guild                              
    presence_count: int

@dataclass
class GuildMember(Disc):
    # the user this guild member represents                                                                                                                                                                                               
    user: User | None = field(kw_only=True, default=None)
    # this user's guild nickname                                                                                                                                                                                                          
    nick: str | None = field(kw_only=True, default=None)
    # the member's `guild avatar hash`                                                                                                                                                                  
    avatar: str | None = field(kw_only=True, default=None)
    # array of `role` object ids                                                                                                                                                                    
    roles: list[Snowflake]
    # when the user joined the guild                                                                                                                                                                                                      
    joined_at: str
    # when the user started `boosting` the guild                                                                                                             
    premium_since: str | None = field(kw_only=True, default=None)
    # whether the user is deafened in voice channels                                                                                                                                                                                      
    deaf: bool
    # whether the user is muted in voice channels                                                                                                                                                                                         
    mute: bool
    # whether the user has not yet passed the guild's `Membership Screening` requirements                                                                                              
    pending: bool | None = field(kw_only=True, default=None)
    # total permissions of the member in the channel, including overwrites, returned when in the interaction object                                                                                                                       
    permissions: str | None = field(kw_only=True, default=None)
    # when the user's `timeout` will expire and the user will be able to communicate in the guild again, null or a time in the past if the user is not timed out
    communication_disabled_until: str | None = field(kw_only=True, default=None)

@dataclass
class Integration(Disc):
    # integration id                                                                 
    id: Snowflake
    # integration name                                                               
    name: str
    # integration type (twitch, youtube, or discord)                                 
    type: str
    # is this integration enabled                                                    
    enabled: bool | None = field(kw_only=True, default=None)
    # is this integration syncing                                                    
    syncing: bool | None = field(kw_only=True, default=None)
    # id that this integration uses for "subscribers"                                
    role_id: Snowflake | None = field(kw_only=True, default=None)
    # whether emoticons should be synced for this integration (twitch only currently)
    enable_emoticons: bool | None = field(kw_only=True, default=None)
    # the behavior of expiring subscribers                                           
    expire_behavior: IntegrationExpireBehavior | None = field(kw_only=True, default=None)
    # the grace period (in days) before expiring subscribers                         
    expire_grace_period: int | None = field(kw_only=True, default=None)
    # user for this integration                                                      
    user: User | None = field(kw_only=True, default=None)
    # integration account information                                                
    account: IntegrationAccount
    # when this integration was last synced                                          
    synced_at: str | None = field(kw_only=True, default=None)
    # how many subscribers this integration has                                      
    subscriber_count: int | None = field(kw_only=True, default=None)
    # has this integration been revoked                                              
    revoked: bool | None = field(kw_only=True, default=None)
    # The bot/OAuth2 application for discord integrations                            
    application: Application | None = field(kw_only=True, default=None)
    # the scopes the application has been authorized for                             
    scopes: list[OAuth2Scope] | None = field(kw_only=True, default=None)

class IntegrationExpireBehavior(int, Enum):
    REMOVE_ROLE = 0
    KICK = 1

@dataclass
class IntegrationAccount(Disc):
    # id of the account  
    id: str
    # name of the account
    name: str

@dataclass
class IntegrationApplication(Disc):
    # the id of the app                                                     
    id: Snowflake
    # the name of the app                                                   
    name: str
    # the `icon hash` of the app          
    icon: str | None
    # the description of the app                                            
    description: str
    # the bot associated with this application                              
    bot: User | None = field(kw_only=True, default=None)

@dataclass
class Ban(Disc):
    # the reason for the ban
    reason: str | None
    # the banned user       
    user: User

@dataclass
class WelcomeScreen(Disc):
    # the server description shown in the welcome screen
    description: str | None
    # the channels shown in the welcome screen, up to 5 
    welcome_channels: list[WelcomeScreenChannel]

@dataclass
class WelcomeScreenChannel(Disc):
    # the channel's id                                                                         
    channel_id: Snowflake
    # the description shown for the channel                                                    
    description: str
    # the `emoji id`, if the emoji is custom                 
    emoji_id: Snowflake | None
    # the emoji name if custom, the unicode character if standard, or `null` if no emoji is set
    emoji_name: str | None

@dataclass
class GuildTemplate(Disc):
    # the template code (unique ID)                         
    code: str
    # template name                                         
    name: str
    # the description for the template                      
    description: str | None
    # number of times this template has been used           
    usage_count: int
    # the ID of the user who created the template           
    creator_id: Snowflake
    # the user who created the template                     
    creator: User
    # when this template was created                        
    created_at: str
    # when this template was last synced to the source guild
    updated_at: str
    # the ID of the guild this template is based on         
    source_guild_id: Snowflake
    # the guild snapshot this template contains             
    serialized_source_guild: Guild
    # whether the template has unsynced changes             
    is_dirty: bool | None

@dataclass
class Emoji(Disc):
    # `emoji id`                             
    id: Snowflake | None
    # emoji name                                                               
    name: str  | None
    # roles allowed to use this emoji                                       
    roles: list[Role] | None = field(kw_only=True, default=None)
    # user that created this emoji                                             
    user: User | None = field(kw_only=True, default=None)
    # whether this emoji must be wrapped in colons                             
    require_colons: bool | None = field(kw_only=True, default=None)
    # whether this emoji is managed                                            
    managed: bool | None = field(kw_only=True, default=None)
    # whether this emoji is animated                                           
    animated: bool | None = field(kw_only=True, default=None)
    # whether this emoji can be used, may be false due to loss of Server Boosts
    available: bool | None = field(kw_only=True, default=None)

class OAuth2Scope(str, Enum):
    # allows your app to fetch data from a user's "Now Playing/Recently Played" list - requires Discord approval
    ACTIVITIES_READ = "activities.read"
    # allows your app to update a user's activity - requires Discord approval (NOT REQUIRED FOR `GAMESDK ACTIVITY MANAGER`
    ACTIVITIES_WRITE = "activities.write"
    # allows your app to read build data for a user's applications
    APPLICATIONS_BUILDS_READ = "applications.builds.read"
    # allows your app to upload/update builds for a user's applications - requires Discord approval
    APPLICATIONS_BUILDS_UPLOAD = "applications.builds.upload"
    # allows your app to use `commands` in a guild
    APPLICATIONS_COMMANDS = "applications.commands"
    # allows your app to update its `commands` only
    APPLICATIONS_COMMANDS_UPDATE = "applications.commands.update"
    # allows your app to update `permissions for its commands` in a guild a user has permissions to
    APPLICATIONS_COMMANDS_PERMISSIONS_UPDATE = "applications.commands.permissions.update"
    # allows your app to read entitlements for a user's applications
    APPLICATIONS_ENTITLEMENTS = "applications.entitlements"
    # allows your app to read and update store data (SKUs, store listings, achievements, etc.) for a user's applications
    APPLICATIONS_STORE_UPDATE = "applications.store.update"
    # for oauth2 bots, this puts the bot in the user's selected guild by default
    BOT = "bot"
    # allows `/users/@me/connections` to return linked third-party accounts
    CONNECTIONS = "connections"
    # allows your app to see information about the user's DMs and group DMs - requires Discord approval
    DM_CHANNELS_READ = "dm_channels.read"
    # enables `/users/@me` to return an `email`
    EMAIL = "email"
    # allows your app to `join users to a group dm`
    GDM_JOIN = "gdm.join"
    # allows `/users/@me/guilds` to return basic information about all of a user's guilds
    GUILDS = "guilds"
    # allows `/guilds/{guild.id}/members/{user.id}` to be used for joining users to a guild
    GUILDS_JOIN = "guilds.join"
    # allows `/users/@me/guilds/{guild.id}/member` to return a user's member information in a guild
    GUILDS_MEMBERS_READ = "guilds.members.read"
    # allows `/users/@me` without `email`
    IDENTIFY = "identify"
    # for local rpc server api access, this allows you to read messages from all client channels (otherwise restricted to channels/guilds your app creates)
    MESSAGES_READ = "messages.read"
    # allows your app to know a user's friends and implicit relationships - requires Discord approval
    RELATIONSHIPS_READ = "relationships.read"
    # for local rpc server access, this allows you to control a user's local Discord client - requires Discord approval
    RPC = "rpc"
    # for local rpc server access, this allows you to update a user's activity - requires Discord approval
    RPC_ACTIVITIES_WRITE = "rpc.activities.write"
    # for local rpc server access, this allows you to receive notifications pushed out to the user - requires Discord approval
    RPC_NOTIFICATIONS_READ = "rpc.notifications.read"
    # for local rpc server access, this allows you to read a user's voice settings and listen for voice events - requires Discord approval
    RPC_VOICE_READ = "rpc.voice.read"
    # for local rpc server access, this allows you to update a user's voice settings - requires Discord approval
    RPC_VOICE_WRITE = "rpc.voice.write"
    # allows your app to connect to voice on user's behalf and see all the voice members - requires Discord approval
    VOICE = "voice"
    # this generates a webhook that is returned in the oauth token response for authorization code grants
    WEBHOOK_INCOMING = "webhook.incoming"

class Permission(int, Enum):
    # Allows creation of instant invites                                                                                                                  | T, V, S
    CREATE_INSTANT_INVITE = 1 << 0
    # Allows kicking members                                                                                                                              |
    KICK_MEMBERS = 1 << 1
    # Allows banning members                                                                                                                              |
    BAN_MEMBERS = 1 << 2
    # Allows all permissions and bypasses channel permission overwrites                                                                                   |
    ADMINISTRATOR = 1 << 3
    # Allows management and editing of channels                                                                                                           | T, V, S
    MANAGE_CHANNELS = 1 << 4
    # Allows management and editing of the guild                                                                                                          |
    MANAGE_GUILD = 1 << 5
    # Allows for the addition of reactions to messages                                                                                                    | T, V
    ADD_REACTIONS = 1 << 6
    # Allows for viewing of audit logs                                                                                                                    |
    VIEW_AUDIT_LOG = 1 << 7
    # Allows for using priority speaker in a voice channel                                                                                                | V
    PRIORITY_SPEAKER = 1 << 8
    # Allows the user to go live                                                                                                                          | V
    STREAM = 1 << 9
    # Allows guild members to view a channel, which includes reading messages in text channels and joining voice channels                                 | T, V, S
    VIEW_CHANNEL = 1 << 10
    # Allows for sending messages in a channel and creating threads in a forum (does not allow sending messages in threads)                               | T, V
    SEND_MESSAGES = 1 << 11
    # Allows for sending of `/tts` messages                                                                                                               | T, V
    SEND_TTS_MESSAGES = 1 << 12
    # Allows for deletion of other users messages                                                                                                         | T, V
    MANAGE_MESSAGES = 1 << 13
    # Links sent by users with this permission will be auto-embedded                                                                                      | T, V
    EMBED_LINKS = 1 << 14
    # Allows for uploading images and files                                                                                                               | T, V
    ATTACH_FILES = 1 << 15
    # Allows for reading of message history                                                                                                               | T, V
    READ_MESSAGE_HISTORY = 1 << 16
    # Allows for using the `@everyone` tag to notify all users in a channel, and the `@here` tag to notify all online users in a channel                  | T, V, S
    MENTION_EVERYONE = 1 << 17
    # Allows the usage of custom emojis from other servers                                                                                                | T, V
    USE_EXTERNAL_EMOJIS = 1 << 18
    # Allows for viewing guild insights                                                                                                                   |
    VIEW_GUILD_INSIGHTS = 1 << 19
    # Allows for joining of a voice channel                                                                                                               | V, S
    CONNECT = 1 << 20
    # Allows for speaking in a voice channel                                                                                                              | V
    SPEAK = 1 << 21
    # Allows for muting members in a voice channel                                                                                                        | V, S
    MUTE_MEMBERS = 1 << 22
    # Allows for deafening of members in a voice channel                                                                                                  | V, S
    DEAFEN_MEMBERS = 1 << 23
    # Allows for moving of members between voice channels                                                                                                 | V, S
    MOVE_MEMBERS = 1 << 24
    # Allows for using voice-activity-detection in a voice channel                                                                                        | V
    USE_VAD = 1 << 25
    # Allows for modification of own nickname                                                                                                             |
    CHANGE_NICKNAME = 1 << 26
    # Allows for modification of other users nicknames                                                                                                    |
    MANAGE_NICKNAMES = 1 << 27
    # Allows management and editing of roles                                                                                                              | T, V, S
    MANAGE_ROLES = 1 << 28
    # Allows management and editing of webhooks                                                                                                           | T, V
    MANAGE_WEBHOOKS = 1 << 29
    # Allows management and editing of emojis and stickers                                                                                                |
    MANAGE_EMOJIS_AND_STICKERS = 1 << 30
    # Allows members to use application commands, including slash commands and context menu commands.                                                     | T, V
    USE_APPLICATION_COMMANDS = 1 << 31
    # Allows for requesting to speak in stage channels. (_This permission is under active development and may be changed or removed._)                    | S
    REQUEST_TO_SPEAK = 1 << 32
    # Allows for creating, editing, and deleting scheduled events                                                                                         | V, S
    MANAGE_EVENTS = 1 << 33
    # Allows for deleting and archiving threads, and viewing all private threads                                                                          | T
    MANAGE_THREADS = 1 << 34
    # Allows for creating public and announcement threads                                                                                                 | T
    CREATE_PUBLIC_THREADS = 1 << 35
    # Allows for creating private threads                                                                                                                 | T
    CREATE_PRIVATE_THREADS = 1 << 36
    # Allows the usage of custom stickers from other servers                                                                                              | T, V
    USE_EXTERNAL_STICKERS = 1 << 37
    # Allows for sending messages in threads                                                                                                              | T
    SEND_MESSAGES_IN_THREADS = 1 << 38
    # Allows for using Activities (applications with the `EMBEDDED` flag) in a voice channel                                                              | V
    USE_EMBEDDED_ACTIVITIES = 1 << 39
    # Allows for timing out users to prevent them from sending or reacting to messages in chat and threads, and from speaking in voice and stage channels |
    MODERATE_MEMBERS = 1 << 40

@dataclass
class Role(Disc):
    # role id                                          
    id: Snowflake
    # role name                                        
    name: str
    # integer representation of hexadecimal color code 
    color: int
    # if this role is pinned in the user listing       
    hoist: bool
    # role unicode emoji                               
    unicode_emoji: str | None = field(kw_only=True, default=None)
    # position of this role                            
    position: int
    # permission bit set                               
    permissions: str
    # whether this role is managed by an integration   
    managed: bool
    # whether this role is mentionable                 
    mentionable: bool
    # the tags this role has                           
    tags: RoleTags | None = field(kw_only=True, default=None)

@dataclass
class RoleTags(Disc):
    # the id of the bot this role belongs to             
    bot_id: Snowflake | None = field(kw_only=True, default=None)
    # the id of the integration this role belongs to     
    integration_id: Snowflake | None = field(kw_only=True, default=None)
    # whether this is the guild's premium subscriber role
    premium_subscriber: bool | None = field(kw_only=True, default=None)

@dataclass
class Team(Disc):
    # description                           
    field: type
    # a hash of the image of the team's icon
    icon: str | None
    # the unique id of the team             
    id: Snowflake
    # the members of the team               
    members: list[TeamMember]
    # the name of the team                  
    name: str
    # the user id of the current team owner 
    owner_user_id: Snowflake

@dataclass
class TeamMember(Disc):
    # description                                                                                    
    field: type
    # the user's `membership state` on the team
    membership_state: MembershipStateType
    # will always be `["*"]`                                                                         
    permissions: list[str]
    # the id of the parent team of which they are a member                                           
    team_id: Snowflake
    # the avatar, discriminator, id, and username of the user                                        
    user: User

class MembershipStateType(int, Enum):
    INVITED = 1
    ACCEPTED = 2


InteractionData = ApplicationCommandData | MessageComponentData | ModalSubmitData
InteractionCallbackData = ResponseMessage | ResponseAutocomplete | ResponseModal
MessageComponent = ActionRow | Button | SelectMenu | TextInput
