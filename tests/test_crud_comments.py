from database_operations import (
    insert_user,
    insert_ticket,
    insert_comment,
    get_comments_for_ticket,
)


def test_insert_comment_and_fetch():
    insert_user("bob", "bob@mail.com", "pass123", "user")
    insert_ticket(1, 1, "Commentable Ticket", "Testing comments")
    insert_comment(1, 1, "Looks good!")

    comments = get_comments_for_ticket(1)
    assert len(comments) == 1
    assert comments[0][3] == "Looks good!"
    assert comments[0][5] == "bob"
