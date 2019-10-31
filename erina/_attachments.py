

class Attachments():
    """Storage for message attachments

    This class is like a temporary storage, for lastest
    received file attachments. File attachments are associated
    to users by user id.
    """

    def __init__(self):
        """Initialize storage.

        Storage is a dict where we have an array of file attachments
        (fbchat attachment objects) associated to user id.
        """
        self.storage = {}

    def reset(self, user):
        """Resets the storage for the specified user.

        Args:
            user (str): User id
        """
        if not user in self.storage.keys():
            return

        self.storage[user] = []

    def add(self, user, attachment):
        """Adds an attachment to the storage of the specified user.

        Args:
            user (str): User id
            attachment (Attachment): fbchat attachment
        """
        if not user in self.storage.keys():
            self.storage[user] = []

        attachment.type = self.type(attachment)
        attachment.author = user

        self.storage[user].append(attachment)

    def get(self, user):
        """Gets the user attachments torage

        Args:
            user (str): User id

        Returns:
            array: attachments array (empty array if there is no attachments)
        """
        if not user in self.storage.keys():
            return []

        return self.storage[user]

    def type(self, attachment):
        """Get the attachment type.

        There is 4 attachment types 'image', 'share', 'file', 'other'.

        Args:
            attachment (Attachment): attachment object

        Returns
            str: attachment type
        """
        type = attachment.__class__.__name__

        if type == "ImageAttachment":
            return "image"

        elif type == "ShareAttachment":
            return "share"

        elif type == "FileAttachment":
            return "file"

        elif type == "AudioAttachment":
            return "audio"

        else:
            return "other"
