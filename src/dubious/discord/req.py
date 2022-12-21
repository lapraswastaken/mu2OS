
from __future__ import annotations

from dataclasses import InitVar, dataclass, field
from typing import Any

from dubious.discord.disc import Disc, Http, HttpReq, Snowflake, cast
from dubious.discord.api import *

@dataclass
class GetGlobalApplicationCommands(HttpReq[list[ApplicationCommand]]):
    @dataclass
    class Query(Disc):
        # Whether to include full localization dictionaries (`name_localizations` and `description_localizations`) in the returned objects, instead of the `name_localized` and `description_localized` fields. Default `false`.
        with_localizations: bool | None = field(kw_only=True, default=None)
    application_id: InitVar[str]
    query: GetGlobalApplicationCommands.Query | None = None

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, application_id: str):
        self.endpoint = f"/applications/{application_id}/commands"

    def cast(self, data: Any):
        return cast(list[ApplicationCommand], data)

@dataclass
class CreateGlobalApplicationCommand(HttpReq[ApplicationCommand]):
    @dataclass
    class Form(Disc):
        # `Name of command`, 1-32 characters                                   
        name: str | None = field(kw_only=True, default=None)
        # Localization dictionary for the `name` field. Values follow the same restrictions as `name`                                                                         
        name_localizations: dict[str, str] | None = field(kw_only=True, default=None)
        # 1-100 character description                                                                                                                                         
        description: str | None = field(kw_only=True, default=None)
        # Localization dictionary for the `description` field. Values follow the same restrictions as `description`                                                           
        description_localizations: dict[str, str] | None = field(kw_only=True, default=None)
        # the parameters for the command                                                                                                                                      
        options: list[ApplicationCommandOption] | None = field(kw_only=True, default=None)
        # Set of `permissions` represented as a bit set                                                                                             
        default_member_permissions: str | None = field(kw_only=True, default=None)
        # Indicates whether the command is available in DMs with the app, only for globally-scoped commands. By default, commands are visible.                                
        dm_permission: bool | None = field(kw_only=True, default=None)
        # Replaced by `default_member_permissions` and will be deprecated in the future. Indicates whether the command is enabled by default when the app is added to a guild.
        default_permission: bool  | None = field(kw_only=True, default=None)
        # Type of command, defaults `1` if not set                                                                                                                            
        type:  ApplicationCommandType | None = field(kw_only=True, default=None)
    application_id: InitVar[str]
    form: CreateGlobalApplicationCommand.Form | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, application_id: str):
        self.endpoint = f"/applications/{application_id}/commands"

    def cast(self, data: Any):
        return cast(ApplicationCommand, data)

@dataclass
class GetGlobalApplicationCommand(HttpReq[ApplicationCommand]):
    application_id: InitVar[str]
    command_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, application_id: str, command_id: str):
        self.endpoint = f"/applications/{application_id}/commands/{command_id}"

    def cast(self, data: Any):
        return cast(ApplicationCommand, data)

@dataclass
class EditGlobalApplicationCommand(HttpReq[ApplicationCommand]):
    @dataclass
    class Form(Disc):
        # `Name of command`, 1-32 characters                                   
        name: str | None = field(kw_only=True, default=None)
        # Localization dictionary for the `name` field. Values follow the same restrictions as `name`                                                                         
        name_localizations: dict[str, str] | None = field(kw_only=True, default=None)
        # 1-100 character description                                                                                                                                         
        description: str | None = field(kw_only=True, default=None)
        # Localization dictionary for the `description` field. Values follow the same restrictions as `description`                                                           
        description_localizations: dict[str, str] | None = field(kw_only=True, default=None)
        # the parameters for the command                                                                                                                                      
        options: list[ApplicationCommandOption] | None = field(kw_only=True, default=None)
        # Set of `permissions` represented as a bit set                                                                                             
        default_member_permissions: str | None = field(kw_only=True, default=None)
        # Indicates whether the command is available in DMs with the app, only for globally-scoped commands. By default, commands are visible.                                
        dm_permission: bool | None = field(kw_only=True, default=None)
        # Replaced by `default_member_permissions` and will be deprecated in the future. Indicates whether the command is enabled by default when the app is added to a guild.
        default_permission: bool  | None = field(kw_only=True, default=None)
    application_id: InitVar[str]
    command_id: InitVar[str]
    form: EditGlobalApplicationCommand.Form | None = None

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, application_id: str, command_id: str):
        self.endpoint = f"/applications/{application_id}/commands/{command_id}"

    def cast(self, data: Any):
        return cast(ApplicationCommand, data)

@dataclass
class DeleteGlobalApplicationCommand(HttpReq[None]):
    application_id: InitVar[str]
    command_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, application_id: str, command_id: str):
        self.endpoint = f"/applications/{application_id}/commands/{command_id}"

    def cast(self, data: Any):
        return None

@dataclass
class BulkOverwriteGlobalApplicationCommands(HttpReq[list[ApplicationCommand]]):
    application_id: InitVar[str]

    method = Http.PUT
    endpoint: str = field(init=False)

    def __post_init__(self, application_id: str):
        self.endpoint = f"/applications/{application_id}/commands"

    def cast(self, data: Any):
        return cast(list[ApplicationCommand], data)

@dataclass
class GetGuildApplicationCommands(HttpReq[list[ApplicationCommand]]):
    @dataclass
    class Query(Disc):
        # Whether to include full localization dictionaries (`name_localizations` and `description_localizations`) in the returned objects, instead of the `name_localized` and `description_localized` fields. Default `false`.
        with_localizations: bool | None = field(kw_only=True, default=None)
    application_id: InitVar[str]
    guild_id: InitVar[str]
    query: GetGuildApplicationCommands.Query | None = None

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, application_id: str, guild_id: str):
        self.endpoint = f"/applications/{application_id}/guilds/{guild_id}/commands"

    def cast(self, data: Any):
        return cast(list[ApplicationCommand], data)

@dataclass
class CreateGuildApplicationCommand(HttpReq[ApplicationCommand]):
    @dataclass
    class Form(Disc):
        # `Name of command`, 1-32 characters                                   
        name: str | None = field(kw_only=True, default=None)
        # Localization dictionary for the `name` field. Values follow the same restrictions as `name`                                                                         
        name_localizations: dict[str, str] | None = field(kw_only=True, default=None)
        # 1-100 character description                                                                                                                                         
        description: str | None = field(kw_only=True, default=None)
        # Localization dictionary for the `description` field. Values follow the same restrictions as `description`                                                           
        description_localizations: dict[str, str] | None = field(kw_only=True, default=None)
        # Parameters for the command                                                                                                                                          
        options: list[ApplicationCommandOption] | None = field(kw_only=True, default=None)
        # Set of `permissions` represented as a bit set                                                                                             
        default_member_permissions: str | None = field(kw_only=True, default=None)
        # Replaced by `default_member_permissions` and will be deprecated in the future. Indicates whether the command is enabled by default when the app is added to a guild.
        default_permission: bool  | None = field(kw_only=True, default=None)
        # Type of command, defaults `1` if not set                                                                                                                            
        type:  ApplicationCommandType | None = field(kw_only=True, default=None)
    application_id: InitVar[str]
    guild_id: InitVar[str]
    form: CreateGuildApplicationCommand.Form | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, application_id: str, guild_id: str):
        self.endpoint = f"/applications/{application_id}/guilds/{guild_id}/commands"

    def cast(self, data: Any):
        return cast(ApplicationCommand, data)

@dataclass
class GetGuildApplicationCommand(HttpReq[ApplicationCommand]):
    application_id: InitVar[str]
    guild_id: InitVar[str]
    command_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, application_id: str, guild_id: str, command_id: str):
        self.endpoint = f"/applications/{application_id}/guilds/{guild_id}/commands/{command_id}"

    def cast(self, data: Any):
        return cast(ApplicationCommand, data)

@dataclass
class EditGuildApplicationCommand(HttpReq[ApplicationCommand]):
    @dataclass
    class Form(Disc):
        # `Name of command`, 1-32 characters                                   
        name: str | None = field(kw_only=True, default=None)
        # Localization dictionary for the `name` field. Values follow the same restrictions as `name`                                                                         
        name_localizations: dict[str, str] | None = field(kw_only=True, default=None)
        # 1-100 character description                                                                                                                                         
        description: str | None = field(kw_only=True, default=None)
        # Localization dictionary for the `description` field. Values follow the same restrictions as `description`                                                           
        description_localizations: dict[str, str] | None = field(kw_only=True, default=None)
        # Parameters for the command                                                                                                                                          
        options: list[ApplicationCommandOption] | None = field(kw_only=True, default=None)
        # Set of `permissions` represented as a bit set                                                                                             
        default_member_permissions: str | None = field(kw_only=True, default=None)
        # Replaced by `default_member_permissions` and will be deprecated in the future. Indicates whether the command is enabled by default when the app is added to a guild.
        default_permission: bool  | None = field(kw_only=True, default=None)
    application_id: InitVar[str]
    guild_id: InitVar[str]
    command_id: InitVar[str]
    form: EditGuildApplicationCommand.Form | None = None

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, application_id: str, guild_id: str, command_id: str):
        self.endpoint = f"/applications/{application_id}/guilds/{guild_id}/commands/{command_id}"

    def cast(self, data: Any):
        return cast(ApplicationCommand, data)

@dataclass
class DeleteGuildApplicationCommand(HttpReq[None]):
    application_id: InitVar[str]
    guild_id: InitVar[str]
    command_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, application_id: str, guild_id: str, command_id: str):
        self.endpoint = f"/applications/{application_id}/guilds/{guild_id}/commands/{command_id}"

    def cast(self, data: Any):
        return None

@dataclass
class BulkOverwriteGuildApplicationCommands(HttpReq[list[ApplicationCommand]]):
    @dataclass
    class Form(Disc):
        # ID of the command, if known                                                                                                                                         
        id: Snowflake | None = field(kw_only=True, default=None)
        # `Name of command`, 1-32 characters                                   
        name: str | None = field(kw_only=True, default=None)
        # Localization dictionary for the `name` field. Values follow the same restrictions as `name`                                                                         
        name_localizations: dict[str, str] | None = field(kw_only=True, default=None)
        # 1-100 character description                                                                                                                                         
        description: str | None = field(kw_only=True, default=None)
        # Localization dictionary for the `description` field. Values follow the same restrictions as `description`                                                           
        description_localizations: dict[str, str] | None = field(kw_only=True, default=None)
        # Parameters for the command                                                                                                                                          
        options: list[ApplicationCommandOption] | None = field(kw_only=True, default=None)
        # Set of `permissions` represented as a bit set                                                                                             
        default_member_permissions: str | None = field(kw_only=True, default=None)
        # Indicates whether the command is available in DMs with the app, only for globally-scoped commands. By default, commands are visible.                                
        dm_permission: bool | None = field(kw_only=True, default=None)
        # Replaced by `default_member_permissions` and will be deprecated in the future. Indicates whether the command is enabled by default when the app is added to a guild.
        default_permission: bool  | None = field(kw_only=True, default=None)
        # Type of command, defaults `1` if not set                                                                                                                            
        type:  ApplicationCommandType | None = field(kw_only=True, default=None)
    application_id: InitVar[str]
    guild_id: InitVar[str]
    form: BulkOverwriteGuildApplicationCommands.Form | None = None

    method = Http.PUT
    endpoint: str = field(init=False)

    def __post_init__(self, application_id: str, guild_id: str):
        self.endpoint = f"/applications/{application_id}/guilds/{guild_id}/commands"

    def cast(self, data: Any):
        return cast(list[ApplicationCommand], data)

@dataclass
class GetGuildApplicationCommandPermissions(HttpReq[list[GuildApplicationCommandPermissions]]):
    application_id: InitVar[str]
    guild_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, application_id: str, guild_id: str):
        self.endpoint = f"/applications/{application_id}/guilds/{guild_id}/commands/permissions"

    def cast(self, data: Any):
        return cast(list[GuildApplicationCommandPermissions], data)

@dataclass
class GetApplicationCommandPermissions(HttpReq[GuildApplicationCommandPermissions]):
    application_id: InitVar[str]
    guild_id: InitVar[str]
    command_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, application_id: str, guild_id: str, command_id: str):
        self.endpoint = f"/applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions"

    def cast(self, data: Any):
        return cast(GuildApplicationCommandPermissions, data)

@dataclass
class EditApplicationCommandPermissions(HttpReq[None]):
    @dataclass
    class Form(Disc):
        # Permissions for the command in the guild
        permissions: list[ApplicationCommandPermission] | None = field(kw_only=True, default=None)
    application_id: InitVar[str]
    guild_id: InitVar[str]
    command_id: InitVar[str]
    form: EditApplicationCommandPermissions.Form | None = None

    method = Http.PUT
    endpoint: str = field(init=False)

    def __post_init__(self, application_id: str, guild_id: str, command_id: str):
        self.endpoint = f"/applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions"

    def cast(self, data: Any):
        return None

@dataclass
class CreateInteractionResponse(HttpReq[None]):

    interaction_id: InitVar[str]
    interaction_token: InitVar[str]
    form: InteractionResponse | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, interaction_id: str, interaction_token: str):
        self.endpoint = f"/interactions/{interaction_id}/{interaction_token}/callback"

    def cast(self, data: Any):
        return None

@dataclass
class CreateStageInstance(HttpReq[StageInstance]):
    @dataclass
    class Form(Disc):
        # The id of the Stage channel                                                                                                       
        channel_id: Snowflake | None = field(kw_only=True, default=None)
        # The topic of the Stage instance (1-120 characters)                                                                                
        topic: str | None = field(kw_only=True, default=None)
        # The `privacy level`
        privacy_level: int | None = field(kw_only=True, default=None)
        # Notify @everyone that a Stage instance has started                                                                                
        send_start_notification: bool | None = field(kw_only=True, default=None)
    form: CreateStageInstance.Form | None = None

    method = Http.POST
    endpoint = "/stage-instances"

    def cast(self, data: Any):
        return cast(StageInstance, data)

@dataclass
class GetStageInstance(HttpReq[None]):
    channel_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/stage-instances/{channel_id}"

    def cast(self, data: Any):
        return None

@dataclass
class ModifyStageInstance(HttpReq[StageInstance]):
    @dataclass
    class Form(Disc):
        # The topic of the Stage instance (1-120 characters)                                                           
        topic: str | None = field(kw_only=True, default=None)
        # The `privacy level` of the Stage instance
        privacy_level: int | None = field(kw_only=True, default=None)
    channel_id: InitVar[str]
    form: ModifyStageInstance.Form | None = None

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/stage-instances/{channel_id}"

    def cast(self, data: Any):
        return cast(StageInstance, data)

@dataclass
class DeleteStageInstance(HttpReq[None]):
    channel_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/stage-instances/{channel_id}"

    def cast(self, data: Any):
        return None

@dataclass
class ListAutoModerationRulesForGuild(HttpReq[list[AutoModerationRule]]):
    guild_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/auto-moderation/rules"

    def cast(self, data: Any):
        return cast(list[AutoModerationRule], data)

@dataclass
class GetAutoModerationRule(HttpReq[AutoModerationRule]):
    guild_id: InitVar[str]
    auto_moderation_rule_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, auto_moderation_rule_id: str):
        self.endpoint = f"/guilds/{guild_id}/auto-moderation/rules/{auto_moderation_rule_id}"

    def cast(self, data: Any):
        return cast(AutoModerationRule, data)

@dataclass
class CreateAutoModerationRule(HttpReq[AutoModerationRule]):
    @dataclass
    class Form(Disc):
        # the rule name                                                                                       
        name: str | None = field(kw_only=True, default=None)
        # the `event type`           
        event_type: int | None = field(kw_only=True, default=None)
        # the `trigger type`       
        trigger_type: int | None = field(kw_only=True, default=None)
        # the `trigger metadata`
        trigger_metadata: object | None = field(kw_only=True, default=None)
        # the actions which will execute when the rule is triggered                                           
        actions: list[AutoModerationAction] | None = field(kw_only=True, default=None)
        # whether the rule is enabled (False by default)                                                      
        enabled: bool | None = field(kw_only=True, default=None)
        # the role ids that should not be affected by the rule (Maximum of 20)                                
        exempt_roles: list[Snowflake] | None = field(kw_only=True, default=None)
        # the channel ids that should not be affected by the rule (Maximum of 50)                             
        exempt_channels: list[Snowflake] | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    form: CreateAutoModerationRule.Form | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/auto-moderation/rules"

    def cast(self, data: Any):
        return cast(AutoModerationRule, data)

@dataclass
class ModifyAutoModerationRule(HttpReq[AutoModerationRule]):
    @dataclass
    class Form(Disc):
        # the rule name                                                                                       
        name: str | None = field(kw_only=True, default=None)
        # the `event type`           
        event_type: int | None = field(kw_only=True, default=None)
        # the `trigger metadata`
        trigger_metadata: object | None = field(kw_only=True, default=None)
        # the actions which will execute when the rule is triggered                                           
        actions: list[AutoModerationAction] | None = field(kw_only=True, default=None)
        # whether the rule is enabled                                                                         
        enabled: bool | None = field(kw_only=True, default=None)
        # the role ids that should not be affected by the rule (Maximum of 20)                                
        exempt_roles: list[Snowflake] | None = field(kw_only=True, default=None)
        # the channel ids that should not be affected by the rule (Maximum of 50)                             
        exempt_channels: list[Snowflake] | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    auto_moderation_rule_id: InitVar[str]
    form: ModifyAutoModerationRule.Form | None = None

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, auto_moderation_rule_id: str):
        self.endpoint = f"/guilds/{guild_id}/auto-moderation/rules/{auto_moderation_rule_id}"

    def cast(self, data: Any):
        return cast(AutoModerationRule, data)

@dataclass
class DeleteAutoModerationRule(HttpReq[None]):
    guild_id: InitVar[str]
    auto_moderation_rule_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, auto_moderation_rule_id: str):
        self.endpoint = f"/guilds/{guild_id}/auto-moderation/rules/{auto_moderation_rule_id}"

    def cast(self, data: Any):
        return None

@dataclass
class GetChannel(HttpReq[Channel]):
    channel_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/channels/{channel_id}"

    def cast(self, data: Any):
        return cast(Channel, data)

@dataclass
class ModifyChannel(HttpReq[Channel]):
    @dataclass
    class Form_GroupDM(Disc):
        # 1-100 character channel name
        name: str | None = field(kw_only=True, default=None)
        # base64 encoded icon         
        icon: bytes | None = field(kw_only=True, default=None)
    @dataclass
    class Form_GuildChannel(Disc):
        # 1-100 character channel name                                                                                                                                                      
        name: str | None = field(kw_only=True, default=None)
        # the `type of channel`; only conversion between text and announcement is supported and only in guilds with the "NEWS" feature
        type: int | None = field(kw_only=True, default=None)
        # the position of the channel in the left-hand listing                                                                                                                              
        position: int | None | None = field(kw_only=True, default=None)
        # 0-1024 character channel topic (0-4096 characters for `GUILD_FORUM` channels)                                                                                                     
        topic: str | None | None = field(kw_only=True, default=None)
        # whether the channel is nsfw                                                                                                                                                       
        nsfw: bool | None | None = field(kw_only=True, default=None)
        # amount of seconds a user has to wait before sending another message (0-21600); bots, as well as users with the permission `manage_messages` or `manage_channel`, are unaffected   
        rate_limit_per_user: int | None | None = field(kw_only=True, default=None)
        # the bitrate (in bits) of the voice or stage channel; min 8000                                                                                                                     
        bitrate: int | None | None = field(kw_only=True, default=None)
        # the user limit of the voice channel; 0 refers to no limit, 1 to 99 refers to a user limit                                                                                         
        user_limit: int | None | None = field(kw_only=True, default=None)
        # channel or category-specific permissions                                                                                                                                          
        permission_overwrites: list[Overwrite] | None = field(kw_only=True, default=None)
        # id of the new parent category for a channel                                                                                                                                       
        parent_id: Snowflake | None | None = field(kw_only=True, default=None)
        # channel `voice region` id, automatic when set to null                                                                                  
        rtc_region: str | None | None = field(kw_only=True, default=None)
        # the camera `video quality mode` of the voice channel                                                                  
        video_quality_mode: int | None | None = field(kw_only=True, default=None)
        # the default duration that the clients use (not the API) for newly created threads in the channel, in minutes, to automatically archive the thread after recent activity           
        default_auto_archive_duration: int | None | None = field(kw_only=True, default=None)
        # `channel flags` is supported.                                           
        flags: int | None = field(kw_only=True, default=None)
        # the set of tags that can be used in a `GUILD_FORUM` channel                                                                                                                       
        available_tags: list[ForumTag] | None = field(kw_only=True, default=None)
        # the emoji to show in the add reaction button on a thread in a `GUILD_FORUM` channel                                                                                               
        default_reaction_emoji: DefaultReaction | None = field(kw_only=True, default=None)
        # the initial `rate_limit_per_user` to set on newly created threads in a channel. this field is copied to the thread at creation time and does not live update.                     
        default_thread_rate_limit_per_user: int | None = field(kw_only=True, default=None)
        # the `default sort order type` used to order posts in `GUILD_FORUM` channels                                              
        default_sort_order: int | None = field(kw_only=True, default=None)
    @dataclass
    class Form_Thread(Disc):
        # 1-100 character channel name                                                                                                                                                                     
        name: str | None = field(kw_only=True, default=None)
        # whether the thread is archived                                                                                                                                                                   
        archived: bool | None = field(kw_only=True, default=None)
        # the thread will stop showing in the channel list after `auto_archive_duration` minutes of inactivity, can be set to: 60, 1440, 4320, 10080                                                       
        auto_archive_duration: int | None = field(kw_only=True, default=None)
        # whether the thread is locked; when a thread is locked, only users with MANAGE_THREADS can unarchive it                                                                                           
        locked: bool | None = field(kw_only=True, default=None)
        # whether non-moderators can add other non-moderators to a thread; only available on private threads                                                                                               
        invitable: bool | None = field(kw_only=True, default=None)
        # amount of seconds a user has to wait before sending another message (0-21600); bots, as well as users with the permission `manage_messages`, `manage_thread`, or `manage_channel`, are unaffected
        rate_limit_per_user: int | None | None = field(kw_only=True, default=None)
        # `channel flags`; `PINNED` can only be set for threads in forum channels  
        flags: int | None = field(kw_only=True, default=None)
        # the IDs of the set of tags that have been applied to a thread in a `GUILD_FORUM` channel                                                                                                         
        applied_tags: list[Snowflake] | None = field(kw_only=True, default=None)
    channel_id: InitVar[str]
    form: ModifyChannel.Form_GroupDM|ModifyChannel.Form_GuildChannel|ModifyChannel.Form_Thread | None = None

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/channels/{channel_id}"

    def cast(self, data: Any):
        return cast(Channel, data)

@dataclass
class DeleteOrCloseChannel(HttpReq[Channel]):
    channel_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/channels/{channel_id}"

    def cast(self, data: Any):
        return cast(Channel, data)

@dataclass
class GetChannelMessages(HttpReq[list[Message]]):
    @dataclass
    class Query(Disc):
        # Get messages around this message ID     
        around: Snowflake | None = field(kw_only=True, default=None)
        # Get messages before this message ID     
        before: Snowflake | None = field(kw_only=True, default=None)
        # Get messages after this message ID      
        after: Snowflake | None = field(kw_only=True, default=None)
        # Max number of messages to return (1-100)
        limit: int | None = field(kw_only=True, default=None)
    channel_id: InitVar[str]
    query: GetChannelMessages.Query | None = None

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/channels/{channel_id}/messages"

    def cast(self, data: Any):
        return cast(list[Message], data)

@dataclass
class GetChannelMessage(HttpReq[Message]):
    channel_id: InitVar[str]
    message_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str, message_id: str):
        self.endpoint = f"/channels/{channel_id}/messages/{message_id}"

    def cast(self, data: Any):
        return cast(Message, data)

@dataclass
class CreateMessage(HttpReq[Message]):
    @dataclass
    class Form(Disc):
        # Message contents (up to 2000 characters)                                                                                                                                   
        content: str | None = field(kw_only=True, default=None)
        # Can be used to verify a message was sent (up to 25 characters). Value will appear in the `Message Create event`.               
        nonce: int | str | None = field(kw_only=True, default=None)
        # `true` if this is a TTS message                                                                                                                                            
        tts: bool | None = field(kw_only=True, default=None)
        # Embedded `rich` content (up to 6000 characters)                                                                                                                            
        embeds: list[Embed] | None = field(kw_only=True, default=None)
        # Allowed mentions for the message                                                                                                                                           
        allowed_mentions: AllowedMentions | None = field(kw_only=True, default=None)
        # Include to make your message a reply                                                                                                                                       
        message_reference: MessageReference | None = field(kw_only=True, default=None)
        # Components to include with the message                                                                                                                                     
        components: list[MessageComponent] | None = field(kw_only=True, default=None)
        # IDs of up to 3 `stickers` in the server to send in the message                                                                     
        sticker_ids: list[Snowflake] | None = field(kw_only=True, default=None)
        # JSON-encoded body of non-file params, only for `multipart/form-data` requests. See `Uploading Files`                                      
        payload_json: str | None = field(kw_only=True, default=None)
        # Attachment objects with filename and description. See `Uploading Files`                                                                   
        attachments: list[Attachment] | None = field(kw_only=True, default=None)
        # `Message flags`
        flags: int | None = field(kw_only=True, default=None)
    channel_id: InitVar[str]
    form: CreateMessage.Form | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/channels/{channel_id}/messages"

    def cast(self, data: Any):
        return cast(Message, data)

@dataclass
class CrosspostMessage(HttpReq[Message]):
    channel_id: InitVar[str]
    message_id: InitVar[str]

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str, message_id: str):
        self.endpoint = f"/channels/{channel_id}/messages/{message_id}/crosspost"

    def cast(self, data: Any):
        return cast(Message, data)

@dataclass
class CreateReaction(HttpReq[None]):
    channel_id: InitVar[str]
    message_id: InitVar[str]
    emoji: InitVar[str]

    method = Http.PUT
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str, message_id: str, emoji: str):
        self.endpoint = f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"

    def cast(self, data: Any):
        return None

@dataclass
class DeleteOwnReaction(HttpReq[None]):
    channel_id: InitVar[str]
    message_id: InitVar[str]
    emoji: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str, message_id: str, emoji: str):
        self.endpoint = f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"

    def cast(self, data: Any):
        return None

@dataclass
class DeleteUserReaction(HttpReq[None]):
    channel_id: InitVar[str]
    message_id: InitVar[str]
    emoji: InitVar[str]
    user_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str, message_id: str, emoji: str, user_id: str):
        self.endpoint = f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/{user_id}"

    def cast(self, data: Any):
        return None

@dataclass
class GetReactions(HttpReq[list[User]]):
    @dataclass
    class Query(Disc):
        # Get users after this user ID         
        after: Snowflake | None = field(kw_only=True, default=None)
        # Max number of users to return (1-100)
        limit: int | None = field(kw_only=True, default=None)
    channel_id: InitVar[str]
    message_id: InitVar[str]
    emoji: InitVar[str]
    query: GetReactions.Query | None = None

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str, message_id: str, emoji: str):
        self.endpoint = f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}"

    def cast(self, data: Any):
        return cast(list[User], data)

@dataclass
class DeleteAllReactions(HttpReq[None]):
    channel_id: InitVar[str]
    message_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str, message_id: str):
        self.endpoint = f"/channels/{channel_id}/messages/{message_id}/reactions"

    def cast(self, data: Any):
        return None

@dataclass
class DeleteAllReactionsForEmoji(HttpReq[None]):
    channel_id: InitVar[str]
    message_id: InitVar[str]
    emoji: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str, message_id: str, emoji: str):
        self.endpoint = f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}"

    def cast(self, data: Any):
        return None

@dataclass
class EditMessage(HttpReq[Message]):
    @dataclass
    class Form(Disc):
        # Message contents (up to 2000 characters)                                                                                               
        content: str | None = field(kw_only=True, default=None)
        # Embedded `rich` content (up to 6000 characters)                                                                                        
        embeds: list[Embed] | None = field(kw_only=True, default=None)
        # Edit the `flags`
        flags: int | None = field(kw_only=True, default=None)
        # Allowed mentions for the message                                                                                                       
        allowed_mentions: AllowedMentions | None = field(kw_only=True, default=None)
        # Components to include with the message                                                                                                 
        components: list[MessageComponent] | None = field(kw_only=True, default=None)
        # JSON-encoded body of non-file params (multipart/form-data only). See `Uploading Files`                
        payload_json: str | None = field(kw_only=True, default=None)
        # Attached files to keep and possible descriptions for new files. See `Uploading Files`                 
        attachments: list[Attachment] | None = field(kw_only=True, default=None)
    channel_id: InitVar[str]
    message_id: InitVar[str]
    form: EditMessage.Form | None = None

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str, message_id: str):
        self.endpoint = f"/channels/{channel_id}/messages/{message_id}"

    def cast(self, data: Any):
        return cast(Message, data)

@dataclass
class DeleteMessage(HttpReq[None]):
    channel_id: InitVar[str]
    message_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str, message_id: str):
        self.endpoint = f"/channels/{channel_id}/messages/{message_id}"

    def cast(self, data: Any):
        return None

@dataclass
class BulkDeleteMessages(HttpReq[None]):
    @dataclass
    class Form(Disc):
        # an array of message ids to delete (2-100)
        messages: list[Snowflake] | None = field(kw_only=True, default=None)
    channel_id: InitVar[str]
    form: BulkDeleteMessages.Form | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/channels/{channel_id}/messages/bulk-delete"

    def cast(self, data: Any):
        return None

@dataclass
class EditChannelPermissions(HttpReq[None]):
    @dataclass
    class Form(Disc):
        # the bitwise value of all allowed permissions (default `"0"`)   
        allow: str | None = field(kw_only=True, default=None)
        # the bitwise value of all disallowed permissions (default `"0"`)
        deny: str | None = field(kw_only=True, default=None)
        # 0 for a role or 1 for a member                                 
        type: int | None = field(kw_only=True, default=None)
    channel_id: InitVar[str]
    overwrite_id: InitVar[str]
    form: EditChannelPermissions.Form | None = None

    method = Http.PUT
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str, overwrite_id: str):
        self.endpoint = f"/channels/{channel_id}/permissions/{overwrite_id}"

    def cast(self, data: Any):
        return None

@dataclass
class GetChannelInvites(HttpReq[list[Invite]]):
    channel_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/channels/{channel_id}/invites"

    def cast(self, data: Any):
        return cast(list[Invite], data)

@dataclass
class CreateChannelInvite(HttpReq[Invite]):
    @dataclass
    class Form(Disc):
        # duration of invite in seconds before expiry, or 0 for never. between 0 and 604800 (7 days)                                               
        max_age: int | None = field(kw_only=True, default=None)
        # max number of uses or 0 for unlimited. between 0 and 100                                                                                 
        max_uses: int | None = field(kw_only=True, default=None)
        # whether this invite only grants temporary membership                                                                                     
        temporary: bool | None = field(kw_only=True, default=None)
        # if true, don't try to reuse a similar invite (useful for creating many unique one time use invites)                                      
        unique: bool | None = field(kw_only=True, default=None)
        # the `type of target` for this voice channel invite                             
        target_type: int | None = field(kw_only=True, default=None)
        # the id of the user whose stream to display for this invite, required if `target_type` is 1, the user must be streaming in the channel    
        target_user_id: Snowflake | None = field(kw_only=True, default=None)
        # the id of the embedded application to open for this invite, required if `target_type` is 2, the application must have the `EMBEDDED` flag
        target_application_id: Snowflake | None = field(kw_only=True, default=None)
    channel_id: InitVar[str]
    form: CreateChannelInvite.Form | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/channels/{channel_id}/invites"

    def cast(self, data: Any):
        return cast(Invite, data)

@dataclass
class DeleteChannelPermission(HttpReq[None]):
    channel_id: InitVar[str]
    overwrite_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str, overwrite_id: str):
        self.endpoint = f"/channels/{channel_id}/permissions/{overwrite_id}"

    def cast(self, data: Any):
        return None

@dataclass
class FollowAnnouncementChannel(HttpReq[FollowedChannel]):
    @dataclass
    class Form(Disc):
        # id of target channel
        webhook_channel_id: Snowflake | None = field(kw_only=True, default=None)
    channel_id: InitVar[str]
    form: FollowAnnouncementChannel.Form | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/channels/{channel_id}/followers"

    def cast(self, data: Any):
        return cast(FollowedChannel, data)

@dataclass
class TriggerTypingIndicator(HttpReq[None]):
    channel_id: InitVar[str]

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/channels/{channel_id}/typing"

    def cast(self, data: Any):
        return None

@dataclass
class GetPinnedMessages(HttpReq[list[Message]]):
    channel_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/channels/{channel_id}/pins"

    def cast(self, data: Any):
        return cast(list[Message], data)

@dataclass
class PinMessage(HttpReq[None]):
    channel_id: InitVar[str]
    message_id: InitVar[str]

    method = Http.PUT
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str, message_id: str):
        self.endpoint = f"/channels/{channel_id}/pins/{message_id}"

    def cast(self, data: Any):
        return None

@dataclass
class UnpinMessage(HttpReq[None]):
    channel_id: InitVar[str]
    message_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str, message_id: str):
        self.endpoint = f"/channels/{channel_id}/pins/{message_id}"

    def cast(self, data: Any):
        return None

@dataclass
class GroupDMAddRecipient(HttpReq[None]):
    @dataclass
    class Form(Disc):
        # access token of a user that has granted your app the `gdm.join` scope
        access_token: str | None = field(kw_only=True, default=None)
        # nickname of the user being added                                     
        nick: str | None = field(kw_only=True, default=None)
    channel_id: InitVar[str]
    user_id: InitVar[str]
    form: GroupDMAddRecipient.Form | None = None

    method = Http.PUT
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str, user_id: str):
        self.endpoint = f"/channels/{channel_id}/recipients/{user_id}"

    def cast(self, data: Any):
        return None

@dataclass
class GroupDMRemoveRecipient(HttpReq[None]):
    channel_id: InitVar[str]
    user_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str, user_id: str):
        self.endpoint = f"/channels/{channel_id}/recipients/{user_id}"

    def cast(self, data: Any):
        return None

@dataclass
class StartThreadFromMessage(HttpReq[Channel]):
    @dataclass
    class Form(Disc):
        # 1-100 character channel name                                                                                                              
        name: str | None = field(kw_only=True, default=None)
        # the thread will stop showing in the channel list after `auto_archive_duration` minutes of inactivity, can be set to: 60, 1440, 4320, 10080
        auto_archive_duration: int | None = field(kw_only=True, default=None)
        # amount of seconds a user has to wait before sending another message (0-21600)                                                             
        rate_limit_per_user: int | None = field(kw_only=True, default=None)
    channel_id: InitVar[str]
    message_id: InitVar[str]
    form: StartThreadFromMessage.Form | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str, message_id: str):
        self.endpoint = f"/channels/{channel_id}/messages/{message_id}/threads"

    def cast(self, data: Any):
        return cast(Channel, data)

@dataclass
class StartThreadWithoutMessage(HttpReq[Channel]):
    @dataclass
    class Form(Disc):
        # 1-100 character channel name                                                                                                              
        name: str | None = field(kw_only=True, default=None)
        # the thread will stop showing in the channel list after `auto_archive_duration` minutes of inactivity, can be set to: 60, 1440, 4320, 10080
        auto_archive_duration: int | None = field(kw_only=True, default=None)
        # the `type of thread` to create                                                      
        type: int | None = field(kw_only=True, default=None)
        # whether non-moderators can add other non-moderators to a thread; only available when creating a private thread                            
        invitable: bool | None = field(kw_only=True, default=None)
        # amount of seconds a user has to wait before sending another message (0-21600)                                                             
        rate_limit_per_user: int | None = field(kw_only=True, default=None)
    channel_id: InitVar[str]
    form: StartThreadWithoutMessage.Form | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/channels/{channel_id}/threads"

    def cast(self, data: Any):
        return cast(Channel, data)

@dataclass
class StartThreadInForumChannel(HttpReq[Channel]):
    @dataclass
    class Form(Disc):
        # 1-100 character channel name                                                                                       
        name: str | None = field(kw_only=True, default=None)
        # duration in minutes to automatically archive the thread after recent activity, can be set to: 60, 1440, 4320, 10080
        auto_archive_duration: int | None = field(kw_only=True, default=None)
        # amount of seconds a user has to wait before sending another message (0-21600)                                      
        rate_limit_per_user: int | None = field(kw_only=True, default=None)
        # contents of the first message in the forum thread                                                                  
        message: ForumThreadMessageParams | None = field(kw_only=True, default=None)
        # the IDs of the set of tags that have been applied to a thread in a `GUILD_FORUM` channel                           
        applied_tags: list[Snowflake] | None = field(kw_only=True, default=None)
    channel_id: InitVar[str]
    form: StartThreadInForumChannel.Form | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/channels/{channel_id}/threads"

    def cast(self, data: Any):
        return cast(Channel, data)

@dataclass
class JoinThread(HttpReq[None]):
    channel_id: InitVar[str]

    method = Http.PUT
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/channels/{channel_id}/thread-members/@me"

    def cast(self, data: Any):
        return None

@dataclass
class AddThreadMember(HttpReq[None]):
    channel_id: InitVar[str]
    user_id: InitVar[str]

    method = Http.PUT
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str, user_id: str):
        self.endpoint = f"/channels/{channel_id}/thread-members/{user_id}"

    def cast(self, data: Any):
        return None

@dataclass
class LeaveThread(HttpReq[None]):
    channel_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/channels/{channel_id}/thread-members/@me"

    def cast(self, data: Any):
        return None

@dataclass
class RemoveThreadMember(HttpReq[None]):
    channel_id: InitVar[str]
    user_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str, user_id: str):
        self.endpoint = f"/channels/{channel_id}/thread-members/{user_id}"

    def cast(self, data: Any):
        return None

@dataclass
class GetThreadMember(HttpReq[ThreadMember]):
    channel_id: InitVar[str]
    user_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str, user_id: str):
        self.endpoint = f"/channels/{channel_id}/thread-members/{user_id}"

    def cast(self, data: Any):
        return cast(ThreadMember, data)

@dataclass
class ListThreadMembers(HttpReq[list[ThreadMember]]):
    channel_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/channels/{channel_id}/thread-members"

    def cast(self, data: Any):
        return cast(list[ThreadMember], data)

@dataclass
class Response_ListPublicArchivedThreads(Disc):
    # the public, archived threads                                                                
    threads: list[Channel] | None = field(kw_only=True, default=None)
    # a thread member object for each returned thread the current user has joined                 
    members: list[ThreadMember] | None = field(kw_only=True, default=None)
    # whether there are potentially additional threads that could be returned on a subsequent call
    has_more: bool | None = field(kw_only=True, default=None)
@dataclass
class ListPublicArchivedThreads(HttpReq[Response_ListPublicArchivedThreads]):
    @dataclass
    class Query(Disc):
        # returns threads before this timestamp       
        before: str | None = field(kw_only=True, default=None)
        # optional maximum number of threads to return
        limit: int | None = field(kw_only=True, default=None)
    channel_id: InitVar[str]
    query: ListPublicArchivedThreads.Query | None = None

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/channels/{channel_id}/threads/archived/public"

    def cast(self, data: Any):
        return cast(Response_ListPublicArchivedThreads, data)

@dataclass
class Response_ListPrivateArchivedThreads(Disc):
    # the private, archived threads                                                               
    threads: list[Channel] | None = field(kw_only=True, default=None)
    # a thread member object for each returned thread the current user has joined                 
    members: list[ThreadMember] | None = field(kw_only=True, default=None)
    # whether there are potentially additional threads that could be returned on a subsequent call
    has_more: bool | None = field(kw_only=True, default=None)
@dataclass
class ListPrivateArchivedThreads(HttpReq[Response_ListPrivateArchivedThreads]):
    @dataclass
    class Query(Disc):
        # returns threads before this timestamp       
        before: str | None = field(kw_only=True, default=None)
        # optional maximum number of threads to return
        limit: int | None = field(kw_only=True, default=None)
    channel_id: InitVar[str]
    query: ListPrivateArchivedThreads.Query | None = None

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/channels/{channel_id}/threads/archived/private"

    def cast(self, data: Any):
        return cast(Response_ListPrivateArchivedThreads, data)

@dataclass
class Response_ListJoinedPrivateArchivedThreads(Disc):
    # the private, archived threads the current user has joined                                   
    threads: list[Channel] | None = field(kw_only=True, default=None)
    # a thread member object for each returned thread the current user has joined                 
    members: list[ThreadMember] | None = field(kw_only=True, default=None)
    # whether there are potentially additional threads that could be returned on a subsequent call
    has_more: bool | None = field(kw_only=True, default=None)
@dataclass
class ListJoinedPrivateArchivedThreads(HttpReq[Response_ListJoinedPrivateArchivedThreads]):
    @dataclass
    class Query(Disc):
        # returns threads before this id              
        before: Snowflake | None = field(kw_only=True, default=None)
        # optional maximum number of threads to return
        limit: int | None = field(kw_only=True, default=None)
    channel_id: InitVar[str]
    query: ListJoinedPrivateArchivedThreads.Query | None = None

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/channels/{channel_id}/users/@me/threads/archived/private"

    def cast(self, data: Any):
        return cast(Response_ListJoinedPrivateArchivedThreads, data)

@dataclass
class GetSticker(HttpReq[Sticker]):
    sticker_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, sticker_id: str):
        self.endpoint = f"/stickers/{sticker_id}"

    def cast(self, data: Any):
        return cast(Sticker, data)

@dataclass
class Response_ListNitroStickerPacks(Disc):
    # The list of `sticker pack`s returned
    sticker_packs: list[StickerPack] | None = field(kw_only=True, default=None)
@dataclass
class ListNitroStickerPacks(HttpReq[Response_ListNitroStickerPacks]):

    method = Http.GET
    endpoint = "/sticker-packs"

    def cast(self, data: Any):
        return cast(Response_ListNitroStickerPacks, data)

@dataclass
class ListGuildStickers(HttpReq[list[Sticker]]):
    guild_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/stickers"

    def cast(self, data: Any):
        return cast(list[Sticker], data)

@dataclass
class GetGuildSticker(HttpReq[Sticker]):
    guild_id: InitVar[str]
    sticker_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, sticker_id: str):
        self.endpoint = f"/guilds/{guild_id}/stickers/{sticker_id}"

    def cast(self, data: Any):
        return cast(Sticker, data)

@dataclass
class CreateGuildSticker(HttpReq[Sticker]):
    @dataclass
    class Form(Disc):
        # name of the sticker (2-30 characters)                                                       
        name: str | None = field(kw_only=True, default=None)
        # description of the sticker (empty or 2-100 characters)                                      
        description: str | None = field(kw_only=True, default=None)
        # autocomplete/suggestion tags for the sticker (max 200 characters)                           
        tags: str | None = field(kw_only=True, default=None)
        # the sticker file to upload, must be a PNG, APNG, or Lottie JSON file, max 500 KB            
        file: Any | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    form: CreateGuildSticker.Form | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/stickers"

    def cast(self, data: Any):
        return cast(Sticker, data)

@dataclass
class ModifyGuildSticker(HttpReq[Sticker]):
    @dataclass
    class Form(Disc):
        # name of the sticker (2-30 characters)                                                       
        name: str | None = field(kw_only=True, default=None)
        # description of the sticker (2-100 characters)                                               
        description: str | None | None = field(kw_only=True, default=None)
        # autocomplete/suggestion tags for the sticker (max 200 characters)                           
        tags: str | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    sticker_id: InitVar[str]
    form: ModifyGuildSticker.Form | None = None

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, sticker_id: str):
        self.endpoint = f"/guilds/{guild_id}/stickers/{sticker_id}"

    def cast(self, data: Any):
        return cast(Sticker, data)

@dataclass
class DeleteGuildSticker(HttpReq[None]):
    guild_id: InitVar[str]
    sticker_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, sticker_id: str):
        self.endpoint = f"/guilds/{guild_id}/stickers/{sticker_id}"

    def cast(self, data: Any):
        return None

@dataclass
class ListScheduledEventsForGuild(HttpReq[list[GuildScheduledEvent]]):
    @dataclass
    class Query(Disc):
        # include number of users subscribed to each event
        with_user_count: bool | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    query: ListScheduledEventsForGuild.Query | None = None

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/scheduled-events"

    def cast(self, data: Any):
        return cast(list[GuildScheduledEvent], data)

@dataclass
class CreateGuildScheduledEvent(HttpReq[GuildScheduledEvent]):
    @dataclass
    class Form(Disc):
        # the channel id of the scheduled event.                                                    
        channel_id: Snowflake  | None = field(kw_only=True, default=None)
        # the entity metadata of the scheduled event                                                
        entity_metadata: GuildScheduledEventEntityMetadata | None = field(kw_only=True, default=None)
        # the name of the scheduled event                                                           
        name: str | None = field(kw_only=True, default=None)
        # the privacy level of the scheduled event                                                  
        privacy_level: GuildScheduledEventPrivacyLevel | None = field(kw_only=True, default=None)
        # the time to schedule the scheduled event                                                  
        scheduled_start_time: str | None = field(kw_only=True, default=None)
        # the time when the scheduled event is scheduled to end                                     
        scheduled_end_time: str | None = field(kw_only=True, default=None)
        # the description of the scheduled event                                                    
        description: str | None = field(kw_only=True, default=None)
        # the entity type of the scheduled event                                                    
        entity_type: GuildScheduledEventEntityType | None = field(kw_only=True, default=None)
        # the cover image of the scheduled event                                                    
        image: str | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    form: CreateGuildScheduledEvent.Form | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/scheduled-events"

    def cast(self, data: Any):
        return cast(GuildScheduledEvent, data)

@dataclass
class GetGuildScheduledEvent(HttpReq[GuildScheduledEvent]):
    @dataclass
    class Query(Disc):
        # include number of users subscribed to this event
        with_user_count: bool | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    guild_scheduled_event_id: InitVar[str]
    query: GetGuildScheduledEvent.Query | None = None

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, guild_scheduled_event_id: str):
        self.endpoint = f"/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}"

    def cast(self, data: Any):
        return cast(GuildScheduledEvent, data)

@dataclass
class ModifyGuildScheduledEvent(HttpReq[GuildScheduledEvent]):
    @dataclass
    class Form(Disc):
        # the channel id of the scheduled event, set to `null` if changing entity type to `EXTERNAL`
        channel_id: Snowflake | None = field(kw_only=True, default=None)
        # the entity metadata of the scheduled event                                                
        entity_metadata: GuildScheduledEventEntityMetadata | None = field(kw_only=True, default=None)
        # the name of the scheduled event                                                           
        name: str | None = field(kw_only=True, default=None)
        # the privacy level of the scheduled event                                                  
        privacy_level: GuildScheduledEventPrivacyLevel | None = field(kw_only=True, default=None)
        # the time to schedule the scheduled event                                                  
        scheduled_start_time: str | None = field(kw_only=True, default=None)
        # the time when the scheduled event is scheduled to end                                     
        scheduled_end_time: str | None = field(kw_only=True, default=None)
        # the description of the scheduled event                                                    
        description: str | None = field(kw_only=True, default=None)
        # the entity type of the scheduled event                                                    
        entity_type: GuildScheduledEventEntityType | None = field(kw_only=True, default=None)
        # the status of the scheduled event                                                         
        status: GuildScheduledEventStatusType | None = field(kw_only=True, default=None)
        # the cover image of the scheduled event                                                    
        image: str | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    guild_scheduled_event_id: InitVar[str]
    form: ModifyGuildScheduledEvent.Form | None = None

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, guild_scheduled_event_id: str):
        self.endpoint = f"/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}"

    def cast(self, data: Any):
        return cast(GuildScheduledEvent, data)

@dataclass
class DeleteGuildScheduledEvent(HttpReq[None]):
    guild_id: InitVar[str]
    guild_scheduled_event_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, guild_scheduled_event_id: str):
        self.endpoint = f"/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}"

    def cast(self, data: Any):
        return None

@dataclass
class GetGuildScheduledEventUsers(HttpReq[list[GuildScheduledEventUser]]):
    @dataclass
    class Query(Disc):
        # number of users to return (up to maximum 100)                                 
        limit: int | None = field(kw_only=True, default=None)
        # include guild member data if it exists                                        
        with_member: bool | None = field(kw_only=True, default=None)
        # consider only users before given user id                                      
        before: Snowflake | None = field(kw_only=True, default=None)
        # consider only users after given user id                                       
        after: Snowflake | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    guild_scheduled_event_id: InitVar[str]
    query: GetGuildScheduledEventUsers.Query | None = None

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, guild_scheduled_event_id: str):
        self.endpoint = f"/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}/users"

    def cast(self, data: Any):
        return cast(list[GuildScheduledEventUser], data)

@dataclass
class CreateWebhook(HttpReq[None]):
    @dataclass
    class Form(Disc):
        # name of the webhook (1-80 characters)
        name: str | None = field(kw_only=True, default=None)
        # image for the default webhook avatar 
        avatar: str | None = field(kw_only=True, default=None)
    channel_id: InitVar[str]
    form: CreateWebhook.Form | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/channels/{channel_id}/webhooks"

    def cast(self, data: Any):
        return None

@dataclass
class GetChannelWebhooks(HttpReq[list[Webhook]]):
    channel_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, channel_id: str):
        self.endpoint = f"/channels/{channel_id}/webhooks"

    def cast(self, data: Any):
        return cast(list[Webhook], data)

@dataclass
class GetGuildWebhooks(HttpReq[list[Webhook]]):
    guild_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/webhooks"

    def cast(self, data: Any):
        return cast(list[Webhook], data)

@dataclass
class GetWebhook(HttpReq[Webhook]):
    webhook_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, webhook_id: str):
        self.endpoint = f"/webhooks/{webhook_id}"

    def cast(self, data: Any):
        return cast(Webhook, data)

@dataclass
class GetWebhookWithToken(HttpReq[None]):
    webhook_id: InitVar[str]
    webhook_token: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, webhook_id: str, webhook_token: str):
        self.endpoint = f"/webhooks/{webhook_id}/{webhook_token}"

    def cast(self, data: Any):
        return None

@dataclass
class ModifyWebhook(HttpReq[Webhook]):
    @dataclass
    class Form(Disc):
        # the default name of the webhook                   
        name: str | None = field(kw_only=True, default=None)
        # image for the default webhook avatar              
        avatar: str | None | None = field(kw_only=True, default=None)
        # the new channel id this webhook should be moved to
        channel_id: Snowflake | None = field(kw_only=True, default=None)
    webhook_id: InitVar[str]
    form: ModifyWebhook.Form | None = None

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, webhook_id: str):
        self.endpoint = f"/webhooks/{webhook_id}"

    def cast(self, data: Any):
        return cast(Webhook, data)

@dataclass
class ModifyWebhookWithToken(HttpReq[None]):
    webhook_id: InitVar[str]
    webhook_token: InitVar[str]

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, webhook_id: str, webhook_token: str):
        self.endpoint = f"/webhooks/{webhook_id}/{webhook_token}"

    def cast(self, data: Any):
        return None

@dataclass
class DeleteWebhook(HttpReq[None]):
    webhook_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, webhook_id: str):
        self.endpoint = f"/webhooks/{webhook_id}"

    def cast(self, data: Any):
        return None

@dataclass
class DeleteWebhookWithToken(HttpReq[None]):
    webhook_id: InitVar[str]
    webhook_token: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, webhook_id: str, webhook_token: str):
        self.endpoint = f"/webhooks/{webhook_id}/{webhook_token}"

    def cast(self, data: Any):
        return None

@dataclass
class ExecuteWebhook(HttpReq[None]):
    @dataclass
    class Query(Disc):
        # waits for server confirmation of message send before response, and returns the created message body (defaults to `false`; when `false` a message that is not saved does not return an error)
        wait: bool | None = field(kw_only=True, default=None)
        # Send a message to the specified thread within a webhook's channel. The thread will automatically be unarchived.
        thread_id: Snowflake | None = field(kw_only=True, default=None)
    @dataclass
    class Form(Disc):
        # the message contents (up to 2000 characters)                                                                                                                               
        content: str | None = field(kw_only=True, default=None)
        # override the default username of the webhook                                                                                                                               
        username: str | None = field(kw_only=True, default=None)
        # override the default avatar of the webhook                                                                                                                                 
        avatar_url: str | None = field(kw_only=True, default=None)
        # true if this is a TTS message                                                                                                                                              
        tts: bool | None = field(kw_only=True, default=None)
        # embedded `rich` content                                                                                                                                                    
        embeds: list[Embed] | None = field(kw_only=True, default=None)
        # allowed mentions for the message                                                                                                                                           
        allowed_mentions: AllowedMentions | None = field(kw_only=True, default=None)
        # the components to include with the message                                                                                                                                 
        components: list[MessageComponent] | None = field(kw_only=True, default=None)
        # JSON encoded body of non-file params                                                                                                                                       
        payload_json: str | None = field(kw_only=True, default=None)
        # attachment objects with filename and description                                                                                                                           
        attachments: list[Attachment] | None = field(kw_only=True, default=None)
        # `message flags`
        flags: int | None = field(kw_only=True, default=None)
        # name of thread to create (requires the webhook channel to be a forum channel)
        thread_name: str | None = field(kw_only=True, default=None)
    webhook_id: InitVar[str]
    webhook_token: InitVar[str]
    query: ExecuteWebhook.Query | None = None
    form: ExecuteWebhook.Form | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, webhook_id: str, webhook_token: str):
        self.endpoint = f"/webhooks/{webhook_id}/{webhook_token}"

    def cast(self, data: Any):
        return None

@dataclass
class ExecuteSlackCompatibleWebhook(HttpReq[None]):
    @dataclass
    class Query(Disc):
        # id of the thread to send the message in                                                                                                              
        thread_id: Snowflake | None = field(kw_only=True, default=None)
        # waits for server confirmation of message send before response (defaults to `true`; when `false` a message that is not saved does not return an error)
        wait: bool | None = field(kw_only=True, default=None)
    webhook_id: InitVar[str]
    webhook_token: InitVar[str]
    query: ExecuteSlackCompatibleWebhook.Query | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, webhook_id: str, webhook_token: str):
        self.endpoint = f"/webhooks/{webhook_id}/{webhook_token}/slack"

    def cast(self, data: Any):
        return None

@dataclass
class ExecuteGitHubCompatibleWebhook(HttpReq[None]):
    @dataclass
    class Query(Disc):
        # id of the thread to send the message in                                                                                                              
        thread_id: Snowflake | None = field(kw_only=True, default=None)
        # waits for server confirmation of message send before response (defaults to `true`; when `false` a message that is not saved does not return an error)
        wait: bool | None = field(kw_only=True, default=None)
    webhook_id: InitVar[str]
    webhook_token: InitVar[str]
    query: ExecuteGitHubCompatibleWebhook.Query | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, webhook_id: str, webhook_token: str):
        self.endpoint = f"/webhooks/{webhook_id}/{webhook_token}/github"

    def cast(self, data: Any):
        return None

@dataclass
class GetWebhookMessage(HttpReq[Message]):
    @dataclass
    class Query(Disc):
        # id of the thread the message is in
        thread_id: Snowflake | None = field(kw_only=True, default=None)
    webhook_id: InitVar[str]
    webhook_token: InitVar[str]
    message_id: InitVar[str]
    query: GetWebhookMessage.Query | None = None

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, webhook_id: str, webhook_token: str, message_id: str):
        self.endpoint = f"/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}"

    def cast(self, data: Any):
        return cast(Message, data)

@dataclass
class EditWebhookMessage(HttpReq[Message]):
    @dataclass
    class Query(Disc):
        # id of the thread the message is in
        thread_id: Snowflake | None = field(kw_only=True, default=None)
    @dataclass
    class Form(Disc):
        # the message contents (up to 2000 characters)                   
        content: str | None = field(kw_only=True, default=None)
        # embedded `rich` content                                        
        embeds: list[Embed] | None = field(kw_only=True, default=None)
        # allowed mentions for the message                               
        allowed_mentions: AllowedMentions | None = field(kw_only=True, default=None)
        # the components to include with the message                     
        components: list[MessageComponent] | None = field(kw_only=True, default=None)
        # JSON encoded body of non-file params (multipart/form-data only)
        payload_json: str | None = field(kw_only=True, default=None)
        # attached files to keep and possible descriptions for new files 
        attachments: list[Attachment] | None = field(kw_only=True, default=None)
    webhook_id: InitVar[str]
    webhook_token: InitVar[str]
    message_id: InitVar[str]
    query: EditWebhookMessage.Query | None = None
    form: EditWebhookMessage.Form | None = None

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, webhook_id: str, webhook_token: str, message_id: str):
        self.endpoint = f"/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}"

    def cast(self, data: Any):
        return cast(Message, data)

@dataclass
class DeleteWebhookMessage(HttpReq[None]):
    @dataclass
    class Query(Disc):
        # id of the thread the message is in
        thread_id: Snowflake | None = field(kw_only=True, default=None)
    webhook_id: InitVar[str]
    webhook_token: InitVar[str]
    message_id: InitVar[str]
    query: DeleteWebhookMessage.Query | None = None

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, webhook_id: str, webhook_token: str, message_id: str):
        self.endpoint = f"/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}"

    def cast(self, data: Any):
        return None

@dataclass
class GetInvite(HttpReq[Invite]):
    @dataclass
    class Query(Disc):
        # whether the invite should contain approximate member counts
        with_counts: bool | None = field(kw_only=True, default=None)
        # whether the invite should contain the expiration date      
        with_expiration: bool | None = field(kw_only=True, default=None)
        # the guild scheduled event to include with the invite       
        guild_scheduled_event_id: Snowflake | None = field(kw_only=True, default=None)
    invite_code: InitVar[str]
    query: GetInvite.Query | None = None

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, invite_code: str):
        self.endpoint = f"/invites/{invite_code}"

    def cast(self, data: Any):
        return cast(Invite, data)

@dataclass
class DeleteInvite(HttpReq[Invite]):
    invite_code: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, invite_code: str):
        self.endpoint = f"/invites/{invite_code}"

    def cast(self, data: Any):
        return cast(Invite, data)

@dataclass
class GetCurrentUser(HttpReq[User]):

    method = Http.GET
    endpoint = "/users/@me"

    def cast(self, data: Any):
        return cast(User, data)

@dataclass
class GetUser(HttpReq[User]):
    user_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, user_id: str):
        self.endpoint = f"/users/{user_id}"

    def cast(self, data: Any):
        return cast(User, data)

@dataclass
class ModifyCurrentUser(HttpReq[User]):
    @dataclass
    class Form(Disc):
        # user's username, if changed may cause the user's discriminator to be randomized.
        username: str | None = field(kw_only=True, default=None)
        # if passed, modifies the user's avatar                                           
        avatar: str | None | None = field(kw_only=True, default=None)
    form: ModifyCurrentUser.Form | None = None

    method = Http.PATCH
    endpoint = "/users/@me"

    def cast(self, data: Any):
        return cast(User, data)

@dataclass
class GetCurrentUserGuilds(HttpReq[list[Guild]]):

    method = Http.GET
    endpoint = "/users/@me/guilds"

    def cast(self, data: Any):
        return cast(list[Guild], data)

@dataclass
class GetCurrentUserGuildMember(HttpReq[GuildMember]):
    guild_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/users/@me/guilds/{guild_id}/member"

    def cast(self, data: Any):
        return cast(GuildMember, data)

@dataclass
class LeaveGuild(HttpReq[None]):
    guild_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/users/@me/guilds/{guild_id}"

    def cast(self, data: Any):
        return None

@dataclass
class CreateDM(HttpReq[Channel]):
    @dataclass
    class Form(Disc):
        # the recipient to open a DM channel with
        recipient_id: Snowflake | None = field(kw_only=True, default=None)
    form: CreateDM.Form | None = None

    method = Http.POST
    endpoint = "/users/@me/channels"

    def cast(self, data: Any):
        return cast(Channel, data)

@dataclass
class CreateGroupDM(HttpReq[Channel]):
    @dataclass
    class Form(Disc):
        # access tokens of users that have granted your app the `gdm.join` scope
        access_tokens: list[str] | None = field(kw_only=True, default=None)
        # a dictionary of user ids to their respective nicknames                
        nicks: dict | None = field(kw_only=True, default=None)
    form: CreateGroupDM.Form | None = None

    method = Http.POST
    endpoint = "/users/@me/channels"

    def cast(self, data: Any):
        return cast(Channel, data)

@dataclass
class GetUserConnections(HttpReq[list[Connection]]):

    method = Http.GET
    endpoint = "/users/@me/connections"

    def cast(self, data: Any):
        return cast(list[Connection], data)

@dataclass
class GetGuildAuditLog(HttpReq[AuditLog]):
    @dataclass
    class Query(Disc):
        # Entries from a specific user ID                                                                            
        user_id: Snowflake | None = field(kw_only=True, default=None)
        # Entries for a specific `audit log event`
        action_type: int | None = field(kw_only=True, default=None)
        # Entries that preceded a specific audit log entry ID                                                        
        before: Snowflake | None = field(kw_only=True, default=None)
        # Maximum number of entries (between 1-100) to return, defaults to 50                                        
        limit: int | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    query: GetGuildAuditLog.Query | None = None

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/audit-logs"

    def cast(self, data: Any):
        return cast(AuditLog, data)

@dataclass
class ListVoiceRegions(HttpReq[list[VoiceRegion]]):

    method = Http.GET
    endpoint = "/voice/regions"

    def cast(self, data: Any):
        return cast(list[VoiceRegion], data)

@dataclass
class CreateGuild(HttpReq[Guild]):
    @dataclass
    class Form(Disc):
        # name of the guild (2-100 characters)                                                                       
        name: str | None = field(kw_only=True, default=None)
        # `voice region`                                   
        region: str | None = field(kw_only=True, default=None)
        # base64 128x128 image for the guild icon                                                                    
        icon: str | None = field(kw_only=True, default=None)
        # `verification level`                                
        verification_level: int | None = field(kw_only=True, default=None)
        # default `message notification level`
        default_message_notifications: int | None = field(kw_only=True, default=None)
        # `explicit content filter level`          
        explicit_content_filter: int | None = field(kw_only=True, default=None)
        # new guild roles                                                                                            
        roles: list[Role] | None = field(kw_only=True, default=None)
        # new guild's channels                                                                                       
        channels: list[Channel] | None = field(kw_only=True, default=None)
        # id for afk channel                                                                                         
        afk_channel_id: Snowflake | None = field(kw_only=True, default=None)
        # afk timeout in seconds, can be set to: 60, 300, 900, 1800, 3600                                           
        afk_timeout: int | None = field(kw_only=True, default=None)
        # the id of the channel where guild notices such as welcome messages and boost events are posted             
        system_channel_id: Snowflake | None = field(kw_only=True, default=None)
        # `system channel flags`                            
        system_channel_flags: int | None = field(kw_only=True, default=None)
    form: CreateGuild.Form | None = None

    method = Http.POST
    endpoint = "/guilds"

    def cast(self, data: Any):
        return cast(Guild, data)

@dataclass
class GetGuild(HttpReq[Guild]):
    @dataclass
    class Query(Disc):
        # when `true`, will return approximate member and presence counts for the guild
        with_counts: bool | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    query: GetGuild.Query | None = None

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}"

    def cast(self, data: Any):
        return cast(Guild, data)

@dataclass
class GetGuildPreview(HttpReq[GuildPreview]):
    guild_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/preview"

    def cast(self, data: Any):
        return cast(GuildPreview, data)

@dataclass
class ModifyGuild(HttpReq[Guild]):
    @dataclass
    class Form(Disc):
        # guild name                                                                                                                                                       
        name: str | None = field(kw_only=True, default=None)
        # guild `voice region`                                                                                  
        region: str | None | None = field(kw_only=True, default=None)
        # `verification level`                                                                                      
        verification_level: int | None | None = field(kw_only=True, default=None)
        # default `message notification level`                                                      
        default_message_notifications: int | None | None = field(kw_only=True, default=None)
        # `explicit content filter level`                                                                
        explicit_content_filter: int | None | None = field(kw_only=True, default=None)
        # id for afk channel                                                                                                                                               
        afk_channel_id: Snowflake | None | None = field(kw_only=True, default=None)
        # afk timeout in seconds, can be set to: 60, 300, 900, 1800, 3600                                                                                                 
        afk_timeout: int | None = field(kw_only=True, default=None)
        # base64 1024x1024 png/jpeg/gif image for the guild icon (can be animated gif when the server has the `ANIMATED_ICON` feature)                                     
        icon: str | None | None = field(kw_only=True, default=None)
        # user id to transfer guild ownership to (must be owner)                                                                                                           
        owner_id: Snowflake | None = field(kw_only=True, default=None)
        # base64 16:9 png/jpeg image for the guild splash (when the server has the `INVITE_SPLASH` feature)                                                                
        splash: str | None | None = field(kw_only=True, default=None)
        # base64 16:9 png/jpeg image for the guild discovery splash (when the server has the `DISCOVERABLE` feature)                                                       
        discovery_splash: str | None | None = field(kw_only=True, default=None)
        # base64 16:9 png/jpeg image for the guild banner (when the server has the `BANNER` feature; can be animated gif when the server has the `ANIMATED_BANNER` feature)
        banner: str | None | None = field(kw_only=True, default=None)
        # the id of the channel where guild notices such as welcome messages and boost events are posted                                                                   
        system_channel_id: Snowflake | None | None = field(kw_only=True, default=None)
        # `system channel flags`                                                                                  
        system_channel_flags: int | None = field(kw_only=True, default=None)
        # the id of the channel where Community guilds display rules and/or guidelines                                                                                     
        rules_channel_id: Snowflake | None | None = field(kw_only=True, default=None)
        # the id of the channel where admins and moderators of Community guilds receive notices from Discord                                                               
        public_updates_channel_id: Snowflake | None | None = field(kw_only=True, default=None)
        # the preferred `locale` of a Community guild used in server discovery and notices from Discord; defaults to "en-US"                      
        preferred_locale: str | None | None = field(kw_only=True, default=None)
        # enabled guild features                                                                                                                                           
        features: list[GuildFeature] | None = field(kw_only=True, default=None)
        # the description for the guild                                                                                                                                    
        description: str | None | None = field(kw_only=True, default=None)
        # whether the guild's boost progress bar should be enabled                                                                                                         
        premium_progress_bar_enabled: bool | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    form: ModifyGuild.Form | None = None

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}"

    def cast(self, data: Any):
        return cast(Guild, data)

@dataclass
class DeleteGuild(HttpReq[None]):
    guild_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}"

    def cast(self, data: Any):
        return None

@dataclass
class GetGuildChannels(HttpReq[list[Channel]]):
    guild_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/channels"

    def cast(self, data: Any):
        return cast(list[Channel], data)

@dataclass
class CreateGuildChannel(HttpReq[Channel]):
    @dataclass
    class Form(Disc):
        # channel name (1-100 characters)                                                                                                                                                
        name: str | None = field(kw_only=True, default=None)
        # the `type of channel`                                                                                                    
        type: int | None = field(kw_only=True, default=None)
        # channel topic (0-1024 characters)                                                                                                                                              
        topic: str | None = field(kw_only=True, default=None)
        # the bitrate (in bits) of the voice or stage channel; min 8000                                                                                                                  
        bitrate: int | None = field(kw_only=True, default=None)
        # the user limit of the voice channel                                                                                                                                            
        user_limit: int | None = field(kw_only=True, default=None)
        # amount of seconds a user has to wait before sending another message (0-21600); bots, as well as users with the permission `manage_messages` or `manage_channel`, are unaffected
        rate_limit_per_user: int | None = field(kw_only=True, default=None)
        # sorting position of the channel                                                                                                                                                
        position: int | None = field(kw_only=True, default=None)
        # the channel's permission overwrites                                                                                                                                            
        permission_overwrites: list[Overwrite] | None = field(kw_only=True, default=None)
        # id of the parent category for a channel                                                                                                                                        
        parent_id: Snowflake | None = field(kw_only=True, default=None)
        # whether the channel is nsfw                                                                                                                                                    
        nsfw: bool | None = field(kw_only=True, default=None)
        # channel `voice region` id of the voice or stage channel, automatic when set to null                                                 
        rtc_region: str | None = field(kw_only=True, default=None)
        # the camera `video quality mode` of the voice channel                                                               
        video_quality_mode: int | None = field(kw_only=True, default=None)
        # the default duration that the clients use (not the API) for newly created threads in the channel, in minutes, to automatically archive the thread after recent activity        
        default_auto_archive_duration: int | None = field(kw_only=True, default=None)
        # emoji to show in the add reaction button on a thread in a `GUILD_FORUM` channel                                                                                                
        default_reaction_emoji: DefaultReaction | None = field(kw_only=True, default=None)
        # set of tags that can be used in a `GUILD_FORUM` channel                                                                                                                        
        available_tags: list[ForumTag] | None = field(kw_only=True, default=None)
        # the `default sort order type` used to order posts in `GUILD_FORUM` channels                                           
        default_sort_order: int | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    form: CreateGuildChannel.Form | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/channels"

    def cast(self, data: Any):
        return cast(Channel, data)

@dataclass
class ModifyGuildChannelPositions(HttpReq[None]):
    @dataclass
    class Form(Disc):
        # channel id                                                                      
        id: Snowflake | None = field(kw_only=True, default=None)
        # sorting position of the channel                                                 
        position: int | None | None = field(kw_only=True, default=None)
        # syncs the permission overwrites with the new parent, if moving to a new category
        lock_permissions: bool | None | None = field(kw_only=True, default=None)
        # the new parent ID for the channel that is moved                                 
        parent_id: Snowflake | None | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    form: ModifyGuildChannelPositions.Form | None = None

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/channels"

    def cast(self, data: Any):
        return None

@dataclass
class Response_ListActiveGuildThreads(Disc):
    # the active threads                                                                          
    threads: list[Channel] | None = field(kw_only=True, default=None)
    # a thread member object for each returned thread the current user has joined                 
    members: list[ThreadMember] | None = field(kw_only=True, default=None)
@dataclass
class ListActiveGuildThreads(HttpReq[Response_ListActiveGuildThreads]):
    guild_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/threads/active"

    def cast(self, data: Any):
        return cast(Response_ListActiveGuildThreads, data)

@dataclass
class GetGuildMember(HttpReq[GuildMember]):
    guild_id: InitVar[str]
    user_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, user_id: str):
        self.endpoint = f"/guilds/{guild_id}/members/{user_id}"

    def cast(self, data: Any):
        return cast(GuildMember, data)

@dataclass
class ListGuildMembers(HttpReq[list[GuildMember]]):
    @dataclass
    class Query(Disc):
        # max number of members to return (1-1000)
        limit: int | None = field(kw_only=True, default=None)
        # the highest user id in the previous page
        after: Snowflake | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    query: ListGuildMembers.Query | None = None

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/members"

    def cast(self, data: Any):
        return cast(list[GuildMember], data)

@dataclass
class SearchGuildMembers(HttpReq[list[GuildMember]]):
    @dataclass
    class Query(Disc):
        # Query string to match username(s) and nickname(s) against.
        query: str | None = field(kw_only=True, default=None)
        # max number of members to return (1-1000)                  
        limit: int | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    query: SearchGuildMembers.Query | None = None

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/members/search"

    def cast(self, data: Any):
        return cast(list[GuildMember], data)

@dataclass
class AddGuildMember(HttpReq[GuildMember]):
    @dataclass
    class Form(Disc):
        # an oauth2 access token granted with the `guilds.join` to the bot's application for the user you want to add to the guild
        access_token: str | None = field(kw_only=True, default=None)
        # value to set user's nickname to                                                                                         
        nick: str | None = field(kw_only=True, default=None)
        # array of role ids the member is assigned                                                                                
        roles: list[Snowflake] | None = field(kw_only=True, default=None)
        # whether the user is muted in voice channels                                                                             
        mute: bool | None = field(kw_only=True, default=None)
        # whether the user is deafened in voice channels                                                                          
        deaf: bool | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    user_id: InitVar[str]
    form: AddGuildMember.Form | None = None

    method = Http.PUT
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, user_id: str):
        self.endpoint = f"/guilds/{guild_id}/members/{user_id}"

    def cast(self, data: Any):
        return cast(GuildMember, data)

@dataclass
class ModifyGuildMember(HttpReq[GuildMember]):
    @dataclass
    class Form(Disc):
        # value to set user's nickname to                                                                                                                                                                                                                                                                                                                  
        nick: str | None = field(kw_only=True, default=None)
        # array of role ids the member is assigned                                                                                                                                                                                                                                                                                                        
        roles: list[Snowflake] | None = field(kw_only=True, default=None)
        # whether the user is muted in voice channels. Will throw a 400 error if the user is not in a voice channel                                                                                                                                                                                                                                        
        mute: bool | None = field(kw_only=True, default=None)
        # whether the user is deafened in voice channels. Will throw a 400 error if the user is not in a voice channel                                                                                                                                                                                                                                    
        deaf: bool | None = field(kw_only=True, default=None)
        # id of channel to move user to (if they are connected to voice)                                                                                                                                                                                                                                                                                  
        channel_id: Snowflake | None = field(kw_only=True, default=None)
        # when the user's `timeout`, set to null to remove timeout. Will throw a 403 error if the user has the ADMINISTRATOR permission or is the owner of the guild
        communication_disabled_until: str | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    user_id: InitVar[str]
    form: ModifyGuildMember.Form | None = None

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, user_id: str):
        self.endpoint = f"/guilds/{guild_id}/members/{user_id}"

    def cast(self, data: Any):
        return cast(GuildMember, data)

@dataclass
class ModifyCurrentMember(HttpReq[None]):
    @dataclass
    class Form(Disc):
        # value to set user's nickname to
        nick: str | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    form: ModifyCurrentMember.Form | None = None

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/members/@me"

    def cast(self, data: Any):
        return None

@dataclass
class ModifyCurrentUserNick(HttpReq[None]):
    @dataclass
    class Form(Disc):
        # value to set user's nickname to
        nick: str | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    form: ModifyCurrentUserNick.Form | None = None

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/members/@me/nick"

    def cast(self, data: Any):
        return None

@dataclass
class AddGuildMemberRole(HttpReq[None]):
    guild_id: InitVar[str]
    user_id: InitVar[str]
    role_id: InitVar[str]

    method = Http.PUT
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, user_id: str, role_id: str):
        self.endpoint = f"/guilds/{guild_id}/members/{user_id}/roles/{role_id}"

    def cast(self, data: Any):
        return None

@dataclass
class RemoveGuildMemberRole(HttpReq[None]):
    guild_id: InitVar[str]
    user_id: InitVar[str]
    role_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, user_id: str, role_id: str):
        self.endpoint = f"/guilds/{guild_id}/members/{user_id}/roles/{role_id}"

    def cast(self, data: Any):
        return None

@dataclass
class RemoveGuildMember(HttpReq[None]):
    guild_id: InitVar[str]
    user_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, user_id: str):
        self.endpoint = f"/guilds/{guild_id}/members/{user_id}"

    def cast(self, data: Any):
        return None

@dataclass
class GetGuildBans(HttpReq[list[Ban]]):
    @dataclass
    class Query(Disc):
        # number of users to return (up to maximum 1000)                                
        limit: int | None = field(kw_only=True, default=None)
        # consider only users before given user id                                      
        before: Snowflake | None = field(kw_only=True, default=None)
        # consider only users after given user id                                       
        after: Snowflake | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    query: GetGuildBans.Query | None = None

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/bans"

    def cast(self, data: Any):
        return cast(list[Ban], data)

@dataclass
class GetGuildBan(HttpReq[Ban]):
    guild_id: InitVar[str]
    user_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, user_id: str):
        self.endpoint = f"/guilds/{guild_id}/bans/{user_id}"

    def cast(self, data: Any):
        return cast(Ban, data)

@dataclass
class CreateGuildBan(HttpReq[None]):
    @dataclass
    class Form(Disc):
        # number of days to delete messages for (0-7) (deprecated)               
        delete_message_days: int | None = field(kw_only=True, default=None)
        # number of seconds to delete messages for, between 0 and 604800 (7 days)
        delete_message_seconds: int | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    user_id: InitVar[str]
    form: CreateGuildBan.Form | None = None

    method = Http.PUT
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, user_id: str):
        self.endpoint = f"/guilds/{guild_id}/bans/{user_id}"

    def cast(self, data: Any):
        return None

@dataclass
class RemoveGuildBan(HttpReq[None]):
    guild_id: InitVar[str]
    user_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, user_id: str):
        self.endpoint = f"/guilds/{guild_id}/bans/{user_id}"

    def cast(self, data: Any):
        return None

@dataclass
class GetGuildRoles(HttpReq[list[Role]]):
    guild_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/roles"

    def cast(self, data: Any):
        return cast(list[Role], data)

@dataclass
class CreateGuildRole(HttpReq[Role]):
    @dataclass
    class Form(Disc):
        # name of the role                                                                                                              
        name: str | None = field(kw_only=True, default=None)
        # bitwise value of the enabled/disabled permissions                                                                             
        permissions: str | None = field(kw_only=True, default=None)
        # RGB color value                                                                                                               
        color: int | None = field(kw_only=True, default=None)
        # whether the role should be displayed separately in the sidebar                                                                
        hoist: bool | None = field(kw_only=True, default=None)
        # the role's icon image (if the guild has the `ROLE_ICONS` feature)                                                             
        icon: str | None | None = field(kw_only=True, default=None)
        # the role's unicode emoji as a `standard emoji`
        unicode_emoji: str | None | None = field(kw_only=True, default=None)
        # whether the role should be mentionable                                                                                        
        mentionable: bool | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    form: CreateGuildRole.Form | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/roles"

    def cast(self, data: Any):
        return cast(Role, data)

@dataclass
class ModifyGuildRolePositions(HttpReq[list[Role]]):
    @dataclass
    class Form(Disc):
        # role                        
        id: Snowflake | None = field(kw_only=True, default=None)
        # sorting position of the role
        position: int | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    form: ModifyGuildRolePositions.Form | None = None

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/roles"

    def cast(self, data: Any):
        return cast(list[Role], data)

@dataclass
class ModifyGuildRole(HttpReq[Role]):
    @dataclass
    class Form(Disc):
        # name of the role                                                                                                              
        name: str | None = field(kw_only=True, default=None)
        # bitwise value of the enabled/disabled permissions                                                                             
        permissions: str | None = field(kw_only=True, default=None)
        # RGB color value                                                                                                               
        color: int | None = field(kw_only=True, default=None)
        # whether the role should be displayed separately in the sidebar                                                                
        hoist: bool | None = field(kw_only=True, default=None)
        # the role's icon image (if the guild has the `ROLE_ICONS` feature)                                                             
        icon: str | None = field(kw_only=True, default=None)
        # the role's unicode emoji as a `standard emoji`
        unicode_emoji: str | None = field(kw_only=True, default=None)
        # whether the role should be mentionable                                                                                        
        mentionable: bool | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    role_id: InitVar[str]
    form: ModifyGuildRole.Form | None = None

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, role_id: str):
        self.endpoint = f"/guilds/{guild_id}/roles/{role_id}"

    def cast(self, data: Any):
        return cast(Role, data)

@dataclass
class ModifyGuildMFALevel(HttpReq[int]):
    @dataclass
    class Form(Disc):
        # `MFA level`                                                                     
        level: int | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    form: ModifyGuildMFALevel.Form | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/mfa"

    def cast(self, data: Any):
        return cast(int, data)

@dataclass
class DeleteGuildRole(HttpReq[None]):
    guild_id: InitVar[str]
    role_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, role_id: str):
        self.endpoint = f"/guilds/{guild_id}/roles/{role_id}"

    def cast(self, data: Any):
        return None

@dataclass
class GetGuildPruneCount(HttpReq[Any]):
    @dataclass
    class Query(Disc):
        # number of days to count prune for (1-30)
        days: int | None = field(kw_only=True, default=None)
        # role(s) to include                      
        include_roles: list[Snowflake] | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    query: GetGuildPruneCount.Query | None = None

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/prune"

    def cast(self, data: Any):
        return cast(Any, data)

@dataclass
class BeginGuildPrune(HttpReq[Any]):
    @dataclass
    class Form(Disc):
        # number of days to prune (1-30)                            
        days: int | None = field(kw_only=True, default=None)
        # whether `pruned` is returned, discouraged for large guilds
        compute_prune_count: bool | None = field(kw_only=True, default=None)
        # role(s) to include                                        
        include_roles: list[Snowflake] | None = field(kw_only=True, default=None)
        # reason for the prune (deprecated)                         
        reason: str | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    form: BeginGuildPrune.Form | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/prune"

    def cast(self, data: Any):
        return cast(Any, data)

@dataclass
class GetGuildVoiceRegions(HttpReq[list[VoiceRegion]]):
    guild_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/regions"

    def cast(self, data: Any):
        return cast(list[VoiceRegion], data)

@dataclass
class GetGuildInvites(HttpReq[list[Invite]]):
    guild_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/invites"

    def cast(self, data: Any):
        return cast(list[Invite], data)

@dataclass
class GetGuildIntegrations(HttpReq[list[Integration]]):
    guild_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/integrations"

    def cast(self, data: Any):
        return cast(list[Integration], data)

@dataclass
class DeleteGuildIntegration(HttpReq[None]):
    guild_id: InitVar[str]
    integration_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, integration_id: str):
        self.endpoint = f"/guilds/{guild_id}/integrations/{integration_id}"

    def cast(self, data: Any):
        return None

@dataclass
class GetGuildWidgetSettings(HttpReq[GuildWidgetSettings]):
    guild_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/widget"

    def cast(self, data: Any):
        return cast(GuildWidgetSettings, data)

@dataclass
class ModifyGuildWidget(HttpReq[GuildWidget]):
    guild_id: InitVar[str]

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/widget"

    def cast(self, data: Any):
        return cast(GuildWidget, data)

@dataclass
class GetGuildWidget(HttpReq[GuildWidget]):
    guild_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/widget_json"

    def cast(self, data: Any):
        return cast(GuildWidget, data)

@dataclass
class GetGuildVanityURL(HttpReq[Invite]):
    guild_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/vanity-url"

    def cast(self, data: Any):
        return cast(Invite, data)

@dataclass
class GetGuildWidgetImage(HttpReq[Any]):
    @dataclass
    class Query(Disc):
        # style of the widget image returned (see below)
        style: str | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    query: GetGuildWidgetImage.Query | None = None

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/widget_png"

    def cast(self, data: Any):
        return cast(Any, data)

@dataclass
class GetGuildWelcomeScreen(HttpReq[WelcomeScreen]):
    guild_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/welcome-screen"

    def cast(self, data: Any):
        return cast(WelcomeScreen, data)

@dataclass
class ModifyGuildWelcomeScreen(HttpReq[WelcomeScreen]):
    @dataclass
    class Form(Disc):
        # whether the welcome screen is enabled                          
        enabled: bool | None = field(kw_only=True, default=None)
        # channels linked in the welcome screen and their display options
        welcome_channels: list[WelcomeScreenChannel] | None = field(kw_only=True, default=None)
        # the server description to show in the welcome screen           
        description: str | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    form: ModifyGuildWelcomeScreen.Form | None = None

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/welcome-screen"

    def cast(self, data: Any):
        return cast(WelcomeScreen, data)

@dataclass
class ModifyCurrentUserVoiceState(HttpReq[None]):
    @dataclass
    class Form(Disc):
        # the id of the channel the user is currently in
        channel_id: Snowflake | None = field(kw_only=True, default=None)
        # toggles the user's suppress state             
        suppress: bool | None = field(kw_only=True, default=None)
        # sets the user's request to speak              
        request_to_speak_timestamp: str | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    form: ModifyCurrentUserVoiceState.Form | None = None

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/voice-states/@me"

    def cast(self, data: Any):
        return None

@dataclass
class ModifyUserVoiceState(HttpReq[None]):
    @dataclass
    class Form(Disc):
        # the id of the channel the user is currently in
        channel_id: Snowflake | None = field(kw_only=True, default=None)
        # toggles the user's suppress state             
        suppress: bool | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    user_id: InitVar[str]
    form: ModifyUserVoiceState.Form | None = None

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, user_id: str):
        self.endpoint = f"/guilds/{guild_id}/voice-states/{user_id}"

    def cast(self, data: Any):
        return None

@dataclass
class GetGuildTemplate(HttpReq[GuildTemplate]):
    template_code: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, template_code: str):
        self.endpoint = f"/guilds/templates/{template_code}"

    def cast(self, data: Any):
        return cast(GuildTemplate, data)

@dataclass
class CreateGuildFromGuildTemplate(HttpReq[Guild]):
    @dataclass
    class Form(Disc):
        # name of the guild (2-100 characters)   
        name: str | None = field(kw_only=True, default=None)
        # base64 128x128 image for the guild icon
        icon: str | None = field(kw_only=True, default=None)
    template_code: InitVar[str]
    form: CreateGuildFromGuildTemplate.Form | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, template_code: str):
        self.endpoint = f"/guilds/templates/{template_code}"

    def cast(self, data: Any):
        return cast(Guild, data)

@dataclass
class GetGuildTemplates(HttpReq[list[GuildTemplate]]):
    guild_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/templates"

    def cast(self, data: Any):
        return cast(list[GuildTemplate], data)

@dataclass
class CreateGuildTemplate(HttpReq[GuildTemplate]):
    @dataclass
    class Form(Disc):
        # name of the template (1-100 characters)        
        name: str | None = field(kw_only=True, default=None)
        # description for the template (0-120 characters)
        description: str | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    form: CreateGuildTemplate.Form | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/templates"

    def cast(self, data: Any):
        return cast(GuildTemplate, data)

@dataclass
class SyncGuildTemplate(HttpReq[GuildTemplate]):
    guild_id: InitVar[str]
    template_code: InitVar[str]

    method = Http.PUT
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, template_code: str):
        self.endpoint = f"/guilds/{guild_id}/templates/{template_code}"

    def cast(self, data: Any):
        return cast(GuildTemplate, data)

@dataclass
class ModifyGuildTemplate(HttpReq[GuildTemplate]):
    @dataclass
    class Form(Disc):
        # name of the template (1-100 characters)        
        name: str | None = field(kw_only=True, default=None)
        # description for the template (0-120 characters)
        description: str | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    template_code: InitVar[str]
    form: ModifyGuildTemplate.Form | None = None

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, template_code: str):
        self.endpoint = f"/guilds/{guild_id}/templates/{template_code}"

    def cast(self, data: Any):
        return cast(GuildTemplate, data)

@dataclass
class DeleteGuildTemplate(HttpReq[GuildTemplate]):
    guild_id: InitVar[str]
    template_code: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, template_code: str):
        self.endpoint = f"/guilds/{guild_id}/templates/{template_code}"

    def cast(self, data: Any):
        return cast(GuildTemplate, data)

@dataclass
class ListGuildEmojis(HttpReq[list[Emoji]]):
    guild_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/emojis"

    def cast(self, data: Any):
        return cast(list[Emoji], data)

@dataclass
class GetGuildEmoji(HttpReq[Emoji]):
    guild_id: InitVar[str]
    emoji_id: InitVar[str]

    method = Http.GET
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, emoji_id: str):
        self.endpoint = f"/guilds/{guild_id}/emojis/{emoji_id}"

    def cast(self, data: Any):
        return cast(Emoji, data)

@dataclass
class CreateGuildEmoji(HttpReq[Emoji]):
    @dataclass
    class Form(Disc):
        # name of the emoji                             
        name: str | None = field(kw_only=True, default=None)
        # the 128x128 emoji image                       
        image: str | None = field(kw_only=True, default=None)
        # roles allowed to use this emoji               
        roles: list[Snowflake] | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    form: CreateGuildEmoji.Form | None = None

    method = Http.POST
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str):
        self.endpoint = f"/guilds/{guild_id}/emojis"

    def cast(self, data: Any):
        return cast(Emoji, data)

@dataclass
class ModifyGuildEmoji(HttpReq[Emoji]):
    @dataclass
    class Form(Disc):
        # name of the emoji                            
        name: str | None = field(kw_only=True, default=None)
        # roles allowed to use this emoji              
        roles: list[Snowflake] | None = field(kw_only=True, default=None)
    guild_id: InitVar[str]
    emoji_id: InitVar[str]
    form: ModifyGuildEmoji.Form | None = None

    method = Http.PATCH
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, emoji_id: str):
        self.endpoint = f"/guilds/{guild_id}/emojis/{emoji_id}"

    def cast(self, data: Any):
        return cast(Emoji, data)

@dataclass
class DeleteGuildEmoji(HttpReq[None]):
    guild_id: InitVar[str]
    emoji_id: InitVar[str]

    method = Http.DELETE
    endpoint: str = field(init=False)

    def __post_init__(self, guild_id: str, emoji_id: str):
        self.endpoint = f"/guilds/{guild_id}/emojis/{emoji_id}"

    def cast(self, data: Any):
        return None

@dataclass
class GetCurrentBotApplicationInformation(HttpReq[Application]):

    method = Http.GET
    endpoint = "/oauth2/applications/@me"

    def cast(self, data: Any):
        return cast(Application, data)

@dataclass
class Response_GetCurrentAuthorizationInformation(Disc):
    # the current application                                                          
    application: Application | None = field(kw_only=True, default=None)
    # the scopes the user has authorized the application for                           
    scopes: list[str] | None = field(kw_only=True, default=None)
    # when the access token expires                                                    
    expires: str | None = field(kw_only=True, default=None)
    # the user who has authorized, if the user has authorized with the `identify` scope
    user: User | None = field(kw_only=True, default=None)
@dataclass
class GetCurrentAuthorizationInformation(HttpReq[Response_GetCurrentAuthorizationInformation]):

    method = Http.GET
    endpoint = "/oauth2/@me"

    def cast(self, data: Any):
        return cast(Response_GetCurrentAuthorizationInformation, data)
