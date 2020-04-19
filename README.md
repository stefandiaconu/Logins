# Logins

This is an application which stores your personal logins for different accounts.

The user has to create a new account which is stored in keychain access on macOS.
The logins are stored in a csv file in the application folder.

In progress:
  - make it available for Windows and Linux (store user's details on keychain equivalent for Windows and Linux)
  - when an entry is edited and submit button is clicked, update the table, don't insert new entry
  - improve search filter (when user deletes from the searchbox, the items in the table appear only when the whole word is deleted)
  - let user to delete selected entry
  - encrypt entries stored in csv file

Possible upgrade: store entries in database
