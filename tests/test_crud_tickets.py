from database_operations import (
    insert_ticket,
    get_ticket,
    get_all_tickets,
    update_ticket_status,
    close_ticket,
    delete_ticket,
)


def test_insert_and_get_ticket():
    insert_ticket(user_id=1, category_id=1, title="Test Ticket", description="Details")
    ticket = get_ticket(1)

    assert ticket is not None
    assert ticket[3] == "Test Ticket"
    assert ticket[4] == "Details"


def test_update_ticket_status():
    insert_ticket(1, 1, "Update Test", "To be updated")
    update_ticket_status(1, "in progress")
    ticket = get_ticket(1)

    assert ticket[5] == "in progress"


def test_close_ticket():
    insert_ticket(1, 1, "Closing Time", "Test")
    close_ticket(1)
    ticket = get_ticket(1)

    assert ticket[5] == "closed"


def test_delete_ticket():
    insert_ticket(1, 1, "Gone Soon", "Test delete")
    delete_ticket(1)
    ticket = get_ticket(1)

    assert ticket is None
