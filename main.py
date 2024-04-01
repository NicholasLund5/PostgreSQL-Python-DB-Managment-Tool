import psycopg2

def connect_to_database():
    try:
        dbconn = psycopg2.connect("host=[hostname] user=[username] " + "password='[password]'")
        return dbconn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def execute_query(conn, query, params=None):
    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            
            if query.strip().lower().startswith("select") or "returning" in query.lower():
                return cur.fetchall()
            else:
                conn.commit()
                return None
    except psycopg2.Error as e:
        print(f"Error executing query: {e}")
        conn.rollback()
        return None
    
#Phase 1
def phase1_menu(conn):
    while True:
        print("----------------------------------------------")
        print("What query would you like to view?\n")
        print("1. Campaigns with the highest number of events")
        print("2. Total amount of expenses for each campaign")
        print("3. Volunteers that have participated in the most events")
        print("4. Campaigns and phases that have not been set up on the website yet (both pushed and not pushed onto the site)")
        print("5. Total amount of donations received for each campaign")
        print("6. Volunteers that have participated in more than three campaigns")
        print("7. Total number of events organized for each event type")
        print("8. What events happened before 2024-06-01")
        print("9. Average salary of all employees")
        print('10. Number of Campaigns that are currently active')
        print('11. Go Back\n')
        choice = input("Enter your choice (1-11): \n")
        queries = {
            '1': "SELECT * FROM Question1;",
            '2': "SELECT * FROM Question2;",
            '3': "SELECT * FROM Question3;",
            '4': "SELECT * FROM Question4;",
            '5': "SELECT * FROM Question5;",
            '6': "SELECT * FROM Question6;",
            '7': "SELECT * FROM Question7;",
            '8': "SELECT * FROM Question8;",
            '9': "SELECT * FROM Question9;",
            '10': "SELECT * FROM Question10;",
        }

        if choice == '11':
            break
        if choice in queries:
            print()
            results = execute_query(conn, queries[choice])
            for row in results:
                formatted_row = ', '.join([str(item) for item in row])
                print(formatted_row)
        else:
            print("Invalid choice. Please enter a number between 1 and 11.")
        print()

#Phase 2 helper functions
    
def initialize_campaign(conn):
    print("Initialize a New Campaign")
    name = input("Enter campaign name: ")

    while True:
        start_date = input("Enter start date (YYYY-MM-DD): ")
        if validate_date(start_date):
            break
        print("Invalid date format. Please use YYYY-MM-DD.")

    while True:
        end_date = input("Enter end date (YYYY-MM-DD): ")
        if validate_date(end_date):
            break
        print("Invalid date format. Please use YYYY-MM-DD.")

    description = input("Enter campaign description: ")

    insert_query = """
    INSERT INTO Campaigns (startDate, endDate, name, description) 
    VALUES (%s, %s, %s, %s);
    """
    execute_query(conn, insert_query, (start_date, end_date, name, description))
    print("Campaign initialized successfully.\n")

def schedule_events(conn):
    print("Schedule a New Event")
    event_type = input("Enter event type: ")

    while True:
        date = input("Enter event date (YYYY-MM-DD): ")
        if validate_date(date):
            break
        print("Invalid date format. Please use YYYY-MM-DD.")

    location = input("Enter event location: ")
    
    print("Available Campaigns:")
    campaigns = execute_query(conn, "SELECT campaignID, name FROM Campaigns;")
    for campaign in campaigns:
        print(f"ID: {campaign[0]}, Name: {campaign[1]}")

    while True:
        try:
            campaign_id = int(input("Select a campaign ID for this event: "))
            if any(campaign[0] == campaign_id for campaign in campaigns):
                break
            print("Invalid campaign ID. Please select from the available campaigns.")
        except ValueError:
            print("Please enter a valid integer for the campaign ID.")

    insert_query = """
    INSERT INTO Events (type, date, location, campaignID) 
    VALUES (%s, %s, %s, %s);
    """
    execute_query(conn, insert_query, (event_type, date, location, campaign_id))
    print("Event scheduled successfully.\n")

def add_volunteer_to_event(conn):
    while True:
        print("Would you like to:\n")
        print("1. Enroll a new volunteer/member and add them to an event")
        print("2. Add a volunteer/member to an event")
        print("3. Go back")
        choice = input("Enter your choice (1-3): \n")
        if choice == '1':
            name = input("Enter new volunteer/member name: \n")
            role_choice = input("Enter role (Volunteer/Member): ").strip().capitalize()
            if role_choice not in ['Volunteer', 'Member']:
                print("Invalid role. Please enter either 'Volunteer' or 'Member'.")
                return

            print('Which event would you like to add %s to?\n' % name)
            events = execute_query(conn, "SELECT * FROM Events;")
            if events:
                for row in events:
                    print(f"Event ID: {row[0]}, Type: {row[1]}, Date: {row[2].strftime('%Y-%m-%d')}, Location: {row[3]}, Campaign ID: {row[4]}")
            else:
                print("No events available.")
            eventID = int(input("Enter event ID: "))
            if eventID not in range(1, len(events) + 1):
                print("\nInvalid event choice.")
            else:
                if role_choice == 'Volunteer':
                    insert_query = "INSERT INTO Members (name, role, numCampaigns, tier) VALUES (%s, 'Volunteer', 1, 1) RETURNING memberID; "
                else:
                    insert_query = "INSERT INTO Members (name, role, numCampaigns, tier) VALUES (%s, 'Member', NULL, NULL) RETURNING memberID; "

                results = execute_query(conn, insert_query, (name,))
                memberID = results[0][0] if results else None
                execute_query(conn, "INSERT INTO MemberEvents (member, eventID) VALUES (%s, %s)", (memberID, eventID))
                print(f"\n{role_choice} added successfully.")

            print()
            break
    
        elif choice == '2':
            print("\nChoose which member or volunteer to assign to an event: \n")

            results = execute_query(conn, "SELECT * FROM Members WHERE role = 'Volunteer' OR role = 'Member';")
            for row in results:
                print(row)
            memberID = int(input("Enter memberID (leftmost value): "))

            if memberID not in [row[0] for row in results]:
                print("\nInvalid member or volunteer choice\n")
            else:
                print('\nWhich event would you like to add them to?\n')
                events = execute_query(conn, "SELECT * FROM Events")
                if events:
                    for event in events:
                        print(f"Event ID: {event[0]}, Type: {event[1]}, Date: {event[2].strftime('%Y-%m-%d')}, Location: {event[3]}")
                else:
                    print("No events found for this campaign.")

                if eventID not in [row[0] for row in results]:
                    print()
                    print("Invalid event choice")
                else:
                    print()
                    execute_query(conn, "INSERT INTO MemberEvents (member, eventID) VALUES (%s, %s)", (memberID, eventID))
                    print("Member/Volunteer added successfully.")

                    role_result = execute_query(conn, "SELECT role FROM Members WHERE memberID = %s;", (memberID,))
                    if role_result and role_result[0][0] == 'Volunteer':
                        numCampaigns_query = execute_query(conn, "SELECT COUNT(DISTINCT e.campaignID) FROM MemberEvents me JOIN Events e ON me.eventID = e.eventID WHERE me.member = %s;", (memberID,))
                        if numCampaigns_query:
                            numCampaigns = numCampaigns_query[0][0]
                            tier = 2 if numCampaigns > 3 else 1
                            execute_query(conn, "UPDATE Members SET numCampaigns = %s, tier = %s WHERE memberID = %s", (numCampaigns, tier, memberID))
                            print(f"Number of campaigns ({numCampaigns}) and tier ({tier}) updated for volunteer.")
                print()
                break
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.\n")
    

def view_campaign(conn):
    print("Available Campaigns:")
    campaigns = execute_query(conn, "SELECT campaignID, name FROM Campaigns;")
    for campaign in campaigns:
        print(f"ID: {campaign[0]}, Name: {campaign[1]}")

    campaign_id = int(input("Enter the campaign ID to view details: "))

    print("\nCampaign Details:")
    campaign_details = execute_query(conn, "SELECT * FROM Campaigns WHERE campaignID = %s;", (campaign_id,))
    if campaign_details:
        for detail in campaign_details:
            print(f"ID: {detail[0]}, Start Date: {detail[1]}, End Date: {detail[2]}, Name: {detail[3]}, Description: {detail[4]}")
    else:
        print("No details found for the selected campaign.")

    print("\nFinancial Details (Costs and Donations):")
    financial_details = execute_query(conn, "SELECT type, amount FROM Finances WHERE campaignID = %s;", (campaign_id,))
    for finance in financial_details:
        print(f"Type: {finance[0]}, Amount: ${finance[1]:,.2f}")

    print("\nEvents in this Campaign:")
    events = execute_query(conn, "SELECT * FROM Events WHERE campaignID = %s;", (campaign_id,))
    for event in events:
        print(f"Event ID: {event[0]}, Type: {event[1]}, Date: {event[2]}, Location: {event[3]}")

    print("\nMembers Assigned to Each Event:")
    for event in events:
        print(f"\nEvent ID: {event[0]} - {event[1]}")
        members = execute_query(conn, "SELECT m.name FROM Members m JOIN MemberEvents me ON m.memberID = me.member WHERE me.eventID = %s;", (event[0],))
        if members:
            for member in members:
                print(f"Member: {member[0]}")
        else:
            print("No members assigned to this event.")

#PHASE 2
def set_up_campaign(conn):
    while True:
        print("----------------------------------")
        print("Please select an option from below\n")
        print("1. Initialize a campaign")
        print("2. Scedule an event")
        print("3. Enroll a new volunteer/member and assign to an event or add a volunteer/member to another event")
        print("4. View the current state of a campaign")
        print("5. Go back")
        choice = input("Enter your choice (1-5): \n")

        if choice == '1':
            initialize_campaign(conn)
        elif choice == '2':
            schedule_events(conn)
        elif choice == '3':
            add_volunteer_to_event(conn)
        elif choice == '4':
            view_campaign(conn)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.\n")

#Phase 3 Helper functions   
def validate_date(date_str):
    parts = date_str.split('-')
    if len(parts) != 3:
        return False

    year, month, day = parts
    if not (year.isdigit() and month.isdigit() and day.isdigit()):
        return False

    try:
        year, month, day = int(year), int(month), int(day)
        return 1 <= month <= 12 and 1 <= day <= 31 and year > 0
    except ValueError:
        return False      
    
def running_balance(conn):
    print("1. Total running balance")
    print("2. Running balance within a date range")
    choice = input("Enter your choice (1-2): ")

    if choice == '1':
        query = """
        SELECT SUM(CASE WHEN type = 'Donation' THEN amount ELSE 0 END) -
               SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END) AS balance
        FROM Finances;
        """
    elif choice == '2':
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        query = """
        SELECT SUM(CASE WHEN type = 'Donation' THEN amount ELSE 0 END) -
               SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END) AS balance
        FROM Finances
        WHERE date BETWEEN %s AND %s;
        """
    else:
        print("Invalid choice.")
        return

    params = (start_date, end_date) if choice == '2' else None
    result = execute_query(conn, query, params)
    if result and result[0][0] is not None:
        balance = result[0][0]
    else:
        balance = 0.0 

    print("\nCurrent Running Balance: ${:.2f}\n".format(balance))

def cost_summary(conn):
    print("1. Total costs summary")
    print("2. Costs summary within a date range")
    choice = input("Enter your choice (1-2): ")

    if choice == '1':
        query = """
        SELECT type, SUM(amount) as total_cost
        FROM Finances
        WHERE type != 'Donation'
        GROUP BY type;
        """
    elif choice == '2':
        while True:
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            if validate_date(start_date) and validate_date(end_date):
                query = """
                SELECT type, SUM(amount) as total_cost
                FROM Finances
                WHERE type != 'Donation' AND date BETWEEN %s AND %s
                GROUP BY type;
                """
                break
            else:
                print("Invalid date format. Please use YYYY-MM-DD.")
    else:
        print("Invalid choice.")
        return

    params = (start_date, end_date) if choice == '2' else None
    results = execute_query(conn, query, params)

    if not results:
        print("No cost data available for the specified period.\n")
        return

    max_cost = max(results, key=lambda x: x[1])[1] if results else 0
    scale = max_cost / 50  
    print("\nCost Summary:")
    for type, total_cost in results:
        bar_chart = '*' * int(total_cost / scale)  
        print(f"{type}: ${total_cost:.2f} [{bar_chart}]")
    print()


def donations_summary(conn):
    print("1. Total donations summary")
    print("2. Donations summary within a date range")
    choice = input("Enter your choice (1-2): ")

    if choice == '1':
        query = """
        SELECT memberID, SUM(amount) as total_donation
        FROM Finances
        WHERE type = 'Donation'
        GROUP BY memberID;
        """
    elif choice == '2':
        while True:
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            if validate_date(start_date) and validate_date(end_date):
                query = """
                SELECT memberID, SUM(amount) as total_donation
                FROM Finances
                WHERE type = 'Donation' AND date BETWEEN %s AND %s
                GROUP BY memberID;
                """
                break
            else:
                print("Invalid date format. Please use YYYY-MM-DD.")
    else:
        print("Invalid choice.")
        return

    params = (start_date, end_date) if choice == '2' else None
    results = execute_query(conn, query, params)

    if not results:
        print("No donation data available for the specified period.\n")
        return
    
    max_donation = max(results, key=lambda x: x[1])[1] if results else 0
    scale = max_donation / 50  
    print("\nDonations Summary:")
    for name, total_donation in results:
        bar_chart = '*' * int(total_donation / scale)  
        print(f"Member: {name}: ${total_donation:.2f} [{bar_chart}]")
    print()

#Phase 3
def show_financial_report(conn):
    while True:
        print("-------------------------------------")
        print("What finances would you like to view?")
        print()
        print("1. Current running balance")
        print("2. Costs")
        print("3. Donations")
        print("4. Go back")
        choice = input("Enter your choice (1-4): ")
        print()

        if choice == '1':
            running_balance(conn)
        elif choice == '2':
            cost_summary(conn)
        elif choice == '3':
            donations_summary(conn)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")
            print()

def log_cost(conn):
    print("-------------------------------------")
    print("Log a Cost\n")
    cost_type = input("Enter cost type (Expense/Rent/Salary): ").strip().capitalize()
    if cost_type not in ['Expense', 'Rent', 'Salary']:
        print("Invalid cost type. Please enter either 'Expense', 'Rent', or 'Salary'.")
        return

    while True:
        try:
            amount = float(input("Enter amount: $"))
            break
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")

    date = input("Enter date (YYYY-MM-DD): ")
    if not validate_date(date):
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    campaign_id, member_id = None, None
    if cost_type == 'Expense':
        print("Available Campaigns:")
        campaigns = execute_query(conn, "SELECT campaignID, name FROM Campaigns;")
        for campaign in campaigns:
            print(f"ID: {campaign[0]}, Name: {campaign[1]}")
        while True:
            try:
                campaign_id = int(input("Enter campaign ID: "))
                if any(campaign[0] == campaign_id for campaign in campaigns):
                    break
                print("Invalid campaign ID. Please select from the available campaigns.")
            except ValueError:
                print("Please enter a valid integer for the campaign ID.")
    elif cost_type == 'Salary':
        print("Available Employees:")
        employees = execute_query(conn, "SELECT memberID, name FROM Members WHERE role = 'Employee';")
        for employee in employees:
            print(f"Member ID: {employee[0]}, Name: {employee[1]}")
        while True:
            try:
                member_id = int(input("Enter member ID: "))
                if any(employee[0] == member_id for employee in employees):
                    break
                print("Invalid member ID. Please select from the available employees.")
            except ValueError:
                print("Please enter a valid integer for the member ID.")

    insert_query = "INSERT INTO Finances (type, amount, date" + (", campaignID" if cost_type == 'Expense' else ", memberID" if cost_type == 'Salary' else "") + ") VALUES (%s, %s, %s" + (", %s" if cost_type in ['Expense', 'Salary'] else "") + ");"
    params = (cost_type, amount, date) + ((campaign_id,) if cost_type == 'Expense' else (member_id,) if cost_type == 'Salary' else ())
    execute_query(conn, insert_query, params)
    print("Cost logged successfully.\n")

def log_donation(conn):
    print("-------------------------------------")
    print("Log a Donation\n")

    while True:
        try:
            amount = float(input("Enter donation amount: $"))
            break
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")

    while True:
        date = input("Enter date (YYYY-MM-DD): ")
        if validate_date(date):
            break
        print("Invalid date format. Please use YYYY-MM-DD.")

    print("Available Campaigns:")
    campaigns = execute_query(conn, "SELECT campaignID, name FROM Campaigns;")
    for campaign in campaigns:
        print(f"ID: {campaign[0]}, Name: {campaign[1]}")
    
    campaign_id = None
    while not campaign_id:
        try:
            campaign_id_input = int(input("Enter campaign ID: "))
            if any(campaign[0] == campaign_id_input for campaign in campaigns):
                campaign_id = campaign_id_input
            else:
                print("Invalid campaign ID. Please select from the available campaigns.")
        except ValueError:
            print("Please enter a valid integer for the campaign ID.")

    print("Available Members:")
    members = execute_query(conn, "SELECT memberID, name FROM Members;")
    for member in members:
        print(f"Member ID: {member[0]}, Name: {member[1]}")
    print("For member not listed, please enroll the member first or leave blank to cancel.")

    member_id = None
    while member_id is None:
        member_id_input = input("Enter donating member ID or leave blank if not listed: ")
        if member_id_input:
            try:
                member_id_input = int(member_id_input)
                if any(member[0] == member_id_input for member in members):
                    member_id = member_id_input
                else:
                    print("Invalid member ID. If the member is not listed, please enroll the member first.")
                    member_id = None
            except ValueError:
                print("Invalid input. Please enter a valid integer for the member ID or leave it blank to cancel.")
                member_id = None
        else:
            print()
            return

    insert_query = "INSERT INTO Finances (type, amount, date, campaignID" + (", memberID" if member_id is not None else "") + ") VALUES ('Donation', %s, %s, %s" + (", %s" if member_id is not None else "") + ");"
    params = (amount, date, campaign_id) + ((member_id,) if member_id is not None else ())
    execute_query(conn, insert_query, params)
    print("Donation logged successfully.\n")

#Phase 4
def browse_membership_history(conn):
    print("\nAvailable Members:\n")
    members = execute_query(conn, "SELECT memberID, name FROM Members;")
    for member in members:
        print(f"Member ID: {member[0]}, Name: {member[1]}")

    member_id = input("Enter member ID to view their history: ")
    try:
        member_id = int(member_id)
        if not any(member[0] == member_id for member in members):
            print("Invalid member ID.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid integer for the member ID.")
        return

    print(f"\nHistory for Member ID {member_id}:")

    history = execute_query(conn, "SELECT e.type, e.date, e.location, c.name FROM MemberEvents me JOIN Events e ON me.eventID = e.eventID JOIN Campaigns c ON e.campaignID = c.campaignID WHERE me.member = %s;", (member_id,))
    for record in history:
        print(f"Event Type: {record[0]}, Date: {record[1]}, Location: {record[2]}, Campaign: {record[3]}")
    print()

def manage_annotations(conn):
    print("\n1. Annotate a Campaign")
    print("2. Annotate a Member Record")
    choice = input("Enter your choice (1-2): \n")

    if choice == '1':
        campaigns = execute_query(conn, "SELECT campaignID, name FROM Campaigns;")
        for campaign in campaigns:
            print(f"ID: {campaign[0]}, Name: {campaign[1]}")

        while True:
            try:
                campaign_id = int(input("Select a campaign ID to annotate: "))
                if any(campaign[0] == campaign_id for campaign in campaigns):
                    break
                print("Invalid campaign ID. Please select from the available campaigns.")
            except ValueError:
                print("Please enter a valid integer for the campaign ID.")

        current_annotation = execute_query(conn, "SELECT annotations FROM Campaigns WHERE campaignID = %s;", (campaign_id,))
        print(f"Current Annotation: {current_annotation[0][0] if current_annotation else 'None'}")
        new_annotation = input("Enter new annotation (This will overwrite existing data): ")
        update_query = "UPDATE Campaigns SET annotations = %s WHERE campaignID = %s;"
        execute_query(conn, update_query, (new_annotation, campaign_id))
        print("Campaign annotation updated.")
    
    elif choice == '2':
        members = execute_query(conn, "SELECT memberID, name FROM Members;")
        for member in members:
            print(f"Member ID: {member[0]}, Name: {member[1]}")
        
        while True:
            try:
                member_id = int(input("Select a member ID to annotate: "))
                if any(member[0] == member_id for member in members):
                    break
                print("Invalid member ID. Please select from the available members.")
            except ValueError:
                print("Please enter a valid integer for the member ID.")

        current_annotation = execute_query(conn, "SELECT annotations FROM Members WHERE memberID = %s;", (member_id,))
        print(f"Current Annotation: {current_annotation[0][0] if current_annotation else 'None'}")
        new_annotation = input("Enter new annotation (This will overwrite existing data): ")
        update_query = "UPDATE Members SET annotations = %s WHERE memberID = %s;"
        execute_query(conn, update_query, (new_annotation, member_id))
        print("Member annotation updated.")
    else:
        print("Invalid choice.")
    print()

def member_engagement_dashboard(conn):
    print("\nMember Engagement Dashboard:\n")
    

    participation_results = execute_query(conn, "SELECT m.name, COUNT(DISTINCT me.eventID) as events_attended, COUNT(DISTINCT e.campaignID) as campaigns_participated FROM Members m LEFT JOIN MemberEvents me ON m.memberID = me.member LEFT JOIN Events e ON me.eventID = e.eventID GROUP BY m.memberID;")
    for member, events_attended, campaigns_participated in participation_results:
        print(f"{member}: Events Attended - {events_attended}, Campaigns Participated - {campaigns_participated}")

    suggestion_results = execute_query(conn, "SELECT m.name, e.type, COUNT(*) as count FROM MemberEvents me JOIN Members m ON me.member = m.memberID JOIN Events e ON me.eventID = e.eventID GROUP BY m.memberID, e.type ORDER BY count DESC LIMIT 5;")
    print("\nTop Member Contributions by Event Type:\n")
    for member, event_type, count in suggestion_results:
        print(f"{member} - {event_type}: {count} times")

    print("\nSuggestion: Members with high participation in certain event types can be approached for similar upcoming events.\n")

def main():
    conn = connect_to_database()
    print("Welcome to the database managment tool.")
    if conn is not None:
        while True:
            print("----------------------------------")
            print("Please select an option from below\n")
            #Phase 1
            print("1. Execute preset queries.")
            #Phase 2
            print("2. Initialize campaign, enroll a volunteer/member and assign them to an event or add volunteers/members to events, scedule events, or view existing campaings.")
            #Phase 3
            print("3. Show financial report.")
            print("4. Log a financial cost.")
            print("5. Log a donation.")
            #Phase 4
            print("6. Browse membership history.")
            print("7. Add member/campaign annotation.")
            #Phase 5
            print("8. Member Engagement Dashboard")
            print("9. Exit")
            choice = input("Enter your choice (1-9): \n")
            if choice == '1':
                phase1_menu(conn)
            elif choice == '2':
                set_up_campaign(conn)
            elif choice == '3':
                show_financial_report(conn)
            elif choice == '4':
                log_cost(conn)
            elif choice == '5':
                log_donation(conn)    
            elif choice == '6':
                browse_membership_history(conn)
            elif choice == '7':
                manage_annotations(conn)
            elif choice == '8':
                member_engagement_dashboard(conn)
            elif choice == '9':
                break
            else:
                print("Invalid choice. Please try again.\n")
        conn.close()
    else:
        print("Failed to connect to the database.")

if __name__ == "__main__":
    main()