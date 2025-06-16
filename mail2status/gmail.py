from simplegmail import Gmail

gmail = Gmail()

def get_gmail_messages(query: str):
    """Fetch unread messages from Gmail with specific criteria."""
    messages = gmail.get_unread_messages(query=query)
    return messages

def mark_as_read(messages):
    for message in messages:
        message.mark_as_read()