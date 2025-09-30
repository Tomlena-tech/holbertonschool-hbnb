# HBnB - **High-Level Package Diagram**

For this task we use a three-tier layered architecture pattern that guarantees separation of **concerns**, **maintainability** and **scalability**.

### 1. Presentation Layer (services/API)

**Purpose:** Handles all user-facing interactions and external communication.

**Responsibilities:**

- Accept HTTP requests from clients
- Validate incoming data
- Delegate business operations to the Business Logic Layer via Facade
- Format and return responses to clients

### **2. Business Logic Layer (Models & Core Logic)**

**Purpose:** Contains the core business rules, domain models, and application logic.

**Responsibilities:**

- Enforce business rules and constraints
- Implement domain-specific logic
- Validate data integrity
- Process complex business operations

### 3. Persistence Layer (Data Access)

**Purpose**: Manages all data storage, retrieval, and database operations.

**Responsibilities**:

- Abstract database access logic
- Execute CRUD (Create, Read, Update, Delete) operations
- Manage database connections and transactions
- Handle data mapping between objects and database tables
- Implement query logic and optimization

### Facade pattern

The Facade pattern acts as a **simplified gateway** between the Presentation Layer and the Business Logic Layer, hiding complexity and providing a clean, easy-to-use interface.

