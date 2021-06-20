# UselessBot
## UselessBot Discord Bot made with Python

<br>

### Installation:
* make sure to have Python 3.9 installed
* run <code>pip install -r requirements.txt</code>
* create a <code>token.txt</code> file and paste your Bot-Token in there
* Change <code>config.json</code> if needed 
* run <code>python3 main.py</code>


### Features
* Modules can always be dynamically enabled and disabled
* Clear Messages
* Join Messages
* Join Roles
* Leveling System
* Minecraft Console Extension
* Moderation (ban, kick, mute)
* Music Bot
* Ping Command
* Prefix Command
* Reaction Roles

### Commands
* Clear
  * clear \<amount\><br>
    Clears a certain amount of Messages<br>
    Parameters: 
      * amount: The amount of messages that should be cleared
* Join Roles
  * joinrole @\<role\>
    <br>Adds a Role to the Join Roles
    <br>Parameters: 
      * role: The Role wich should be given on Join
* Leveling System
  * add-level @\<member\> \<level\><br>
    Adds Levels to a User<br>
    Parameters:
    * member: The Member to add the Levels to
    * level: The amount of Levels that should be given to the Member
  * remove-level @\<member\> \<level\><br>
    Removes Levels from a User<br>
    Parameters:
    * member: The Member to remove the Levels from
    * level: THe amount of Levels that should be removed from the Member
  * reset-level @\<member\><br>
    Resets the Levels from a User<br>
    Parameters:
    * member: The Member to reset the Levels from
* Moderation
  * ban @\<member\> [reason]<br>
    Bans a User<br>
    Parameter:
    * member: The member wich should be banned
    * reason: The Reason the member should be banned
  * unban \<member\><br>
    Unbans a User<br>
    Parameter:
    * member: The Reason the member should be unbanned
  * kick @\<member\> [reason]<br>
    Kicks a User<br>
    Parameter: 
    * member: The Member wich should be kicked
    * reason: The Reason the member should be kicked
  * mute @\<member\> [reason]<br>
    Mutes a user <br>
    Parameters: 
    * member: The Member wich should be muted
    * reason: The Reason the member should be muted
  * unmute @\<member\><br>
    Unmutes a User<br>
    Parameters:
    * member: The Member wich should be unmuted
  * createmuterole <name><br>
    Creates a Mute Role<br>
    Parameters: 
    * name: The Name of the Muterole that should be created
* Modules
  * load-module \<name\><br>
  Loads a Module<br>
  Parameters:
    * name: The Name of the Module that should be loaded
  * unload-module \<name\><br>
  Unloads a Module<br>
  Parameters:
    * name: The name of the Module that should be unloaded
  * list-modules<br>
    Lists all Modules<br>
  * reload-module \<name\><br>
  Reloads a Module<br>
  Parameters: 
    * name: The name of the Module that should be reloaded
  * reload-modules<br>
  Reloads all Modules
* Music
  * join [channel]<br>
  Joins the Bot to either the channel you are currently in, or the Channel you specified<br>
    Parameters:
    * channel: The Channel the Bot should join in, ignored if you are already in a voice channel
  * leave<br>
    Disconnects the Bot from the Channel
  * play \<url\><br>
    Plays a Song from the given URL<br>
    Parameters:
    * url: The URL of the Song
  * volume \<volume\><br>
    Changes the Volume to the given Volume<br>
    Parameters:
    * volume: The volume the Bot should change to (number between 1 and 100)
  * stop<br>
    Stops the playing Song
  * pause<br>
  Pauses the playing Song
  * resume<br>
  Resumes the playing Song
* Ping
  * ping<br>
  Command for checking if the bot is online
* Prefix
  * prefix \<new prefix\><br>
  Changes the Prefix to a new, given Prefix<br>
  Parameters:
    * new prefix: The new Prefix of the Bot
* Reaction Roles
  * reactrole [message id] [emoji] [role id]
  Adds a new Reaction Role to the Bot<br>
  Parameters:
    * message id: Has to be provided if the Command isn´t a reply
    * emoji: The emoji wich should give the Role when a user reacts to it
    * role id: Has to be provided if there isn´t a mentioned Role in the Command
