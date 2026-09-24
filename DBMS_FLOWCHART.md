# DBMS Project Flowchart

## 1. Overall system flow

```mermaid
flowchart TD
    A[User / Browser] --> B[Django URL Router]
    B --> C[View Function]
    C --> D{Operation}

    D -->|Insert user| E[Validate form data]
    E -->|Valid and unique ID| F[ Django ORM: User.objects.create ]
    E -->|Invalid or duplicate| G[Return error message]
    F --> H[(SQLite database: db.sqlite3)]

    D -->|Show or sort users| I[Django ORM: SELECT User]
    I --> H
    H --> J[Render HTML table]

    D -->|Edit user| K[Django ORM: SELECT by user_id]
    K --> H
    K --> L[Validate updated fields]
    L --> M[Django ORM: UPDATE User]
    M --> H

    D -->|Delete user| N[Django ORM: DELETE User]
    N --> H

    D -->|Run custom SQL| O[Validate SQL input]
    O -->|Only one SELECT, INSERT, UPDATE, or DELETE| P[Database cursor executes raw SQL]
    O -->|DDL, multiple statements, or invalid command| G
    P --> H
    P --> Q[Display rows or affected-row result]

    H --> R[Generate users.csv]
    R --> S[CSV download / external copy]
```

## 2. Database design / ER view

```mermaid
erDiagram
    USER {
        int user_id PK
        varchar user_name
        varchar country
        int u_age
        varchar pincode
        varchar city
        varchar passwords
    }

    GAME {
        int game_id PK
        int user_id FK
        varchar game_name
        varchar game_type
        int age_rest
        int rate
    }

    USER ||--o{ GAME : has
```

### DBMS interpretation

- `User` is the main entity and uses `user_id` as its primary key.
- `Game` uses `game_id` as its primary key and stores `user_id` to associate games with users.
- The supplied `_database.sql` declares `Game.user_id` as a foreign key referencing `User.user_id`.
- In the current Django model and migration, `Game.user_id` is an `IntegerField`, so Django does not currently enforce that relationship as a `ForeignKey`. The relationship is therefore logical in the running Django application unless the database was created from `_database.sql`.
- The database engine configured for the application is SQLite, stored in `db.sqlite3`.

## 3. CRUD and query flow

```mermaid
flowchart LR
    U[User action] --> V[Django view]
    V --> W{Database operation}

    W -->|Create| C[INSERT into User]
    W -->|Read| R[SELECT from User or Game]
    W -->|Update| D[UPDATE User]
    W -->|Delete| X[DELETE from User]

    C --> DB[(SQLite DBMS)]
    R --> DB
    D --> DB
    X --> DB

    DB --> OUT[HTML response]
    DB --> CSV[users.csv synchronization for SQL data changes]
```

## 4. Custom SQL safety flow

```mermaid
flowchart TD
    A[User enters SQL query] --> B{Starts with SELECT,
    INSERT, UPDATE, or DELETE?}
    B -->|No| X[Reject query]
    B -->|Yes| C{Contains blocked keyword
    or multiple statements?}
    C -->|Yes| X
    C -->|No| D[Run inside transaction.atomic]
    D --> E{Statement type}
    E -->|SELECT| F[Fetch columns and rows]
    E -->|INSERT / UPDATE / DELETE| G[Commit data change]
    G --> H[Regenerate users.csv]
    F --> I[Render query results]
    H --> I
    X --> J[Render security error]
```

## Short presentation explanation

This project is a database-driven Django web application. The browser sends a request to a Django URL, the URL selects a view, and the view performs database operations through either the Django ORM or a controlled raw SQL cursor. SQLite stores the persistent records in two main tables: `User` and `Game`. The application supports the four DBMS CRUD operations: inserting, selecting, updating, and deleting records. It also demonstrates sorting, filtering, joining `User` and `Game`, transactions, primary keys, and the intended foreign-key relationship. After data-changing SQL operations, the current `User` records are synchronized to `users.csv` for export; the CSV is a copy of the database data, not the primary database.

## Suggested title for a report

**DBMS-Based User and Game Management System Using Django and SQLite**
