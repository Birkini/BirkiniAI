-- Create the database for Birkini
CREATE DATABASE birkini;

-- Use the Birkini database
USE birkini;

-- Create Users table
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique user identifier
    username VARCHAR(100) NOT NULL UNIQUE,   -- Username for login
    email VARCHAR(150) NOT NULL UNIQUE,      -- User email (used for authentication)
    password_hash VARCHAR(255) NOT NULL,     -- Password hash for secure storage
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Account creation time
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- Account update time
    last_login TIMESTAMP,  -- Time of last login
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active' -- User account status
);

-- Create Transactions table
CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique transaction identifier
    user_id INT,  -- Foreign key referencing Users table
    amount DECIMAL(10, 2) NOT NULL,  -- Transaction amount
    transaction_type ENUM('deposit', 'withdrawal', 'transfer') NOT NULL,  -- Type of transaction
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Transaction time
    status ENUM('pending', 'completed', 'failed') DEFAULT 'pending',  -- Transaction status
    FOREIGN KEY (user_id) REFERENCES Users(user_id)  -- Link to the Users table
);

-- Create Backups table (for storing backup details)
CREATE TABLE Backups (
    backup_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique backup identifier
    user_id INT,  -- Foreign key referencing Users table (the user who created the backup)
    backup_type ENUM('full', 'incremental') NOT NULL,  -- Type of backup
    file_location VARCHAR(255) NOT NULL,  -- File path or URL to the backup location
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Time of backup creation
    status ENUM('completed', 'failed') DEFAULT 'completed',  -- Status of the backup
    FOREIGN KEY (user_id) REFERENCES Users(user_id)  -- Link to the Users table
);

-- Create Audit Logs table (for tracking system events and actions)
CREATE TABLE AuditLogs (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique audit log identifier
    user_id INT,  -- Foreign key referencing Users table
    action VARCHAR(255) NOT NULL,  -- Description of the action (e.g., login, file upload)
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Time of the action
    ip_address VARCHAR(50),  -- IP address of the user performing the action
    status ENUM('success', 'failure') DEFAULT 'success',  -- Status of the action
    FOREIGN KEY (user_id) REFERENCES Users(user_id)  -- Link to the Users table
);

-- Create a table for storing system settings
CREATE TABLE SystemSettings (
    setting_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique setting identifier
    setting_name VARCHAR(100) NOT NULL UNIQUE,  -- Name of the setting
    setting_value TEXT NOT NULL,  -- Value of the setting
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Time of creation
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- Time of last update
);

-- Create a table for storing API rate limits (if applicable)
CREATE TABLE APIRateLimits (
    rate_limit_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique rate limit identifier
    user_id INT,  -- Foreign key referencing Users table
    requests_made INT DEFAULT 0,  -- Number of requests made by the user
    last_reset TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Time when the request count was last reset
    FOREIGN KEY (user_id) REFERENCES Users(user_id)  -- Link to the Users table
);

-- Create an example table for storing user data (e.g., user profile information)
CREATE TABLE UserProfile (
    profile_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique profile identifier
    user_id INT,  -- Foreign key referencing Users table
    bio TEXT,  -- User biography
    profile_picture_url VARCHAR(255),  -- URL to the user's profile picture
    social_links JSON,  -- JSON field to store social media links
    FOREIGN KEY (user_id) REFERENCES Users(user_id)  -- Link to the Users table
);

-- Insert example user data
INSERT INTO Users (username, email, password_hash, status)
VALUES ('alice', 'alice@example.com', 'hashed_password_123', 'active'),
       ('bob', 'bob@example.com', 'hashed_password_456', 'active');

-- Insert example transaction data
INSERT INTO Transactions (user_id, amount, transaction_type, status)
VALUES (1, 100.00, 'deposit', 'completed'),
       (2, 50.50, 'withdrawal', 'completed');

-- Insert example backup data
INSERT INTO Backups (user_id, backup_type, file_location)
VALUES (1, 'full', '/backups/backup_2023_01_01.zip'),
       (2, 'incremental', '/backups/backup_2023_01_02.zip');

-- Insert example audit log data
INSERT INTO AuditLogs (user_id, action, ip_address, status)
VALUES (1, 'login', '192.168.1.1', 'success'),
       (2, 'file upload', '192.168.1.2', 'failure');

-- Insert example system setting
INSERT INTO SystemSettings (setting_name, setting_value)
VALUES ('max_file_upload_size', '50MB'),
       ('default_language', 'English');

-- Insert example API rate limit data
INSERT INTO APIRateLimits (user_id, requests_made)
VALUES (1, 50),
       (2, 10);

-- Insert example user profile data
INSERT INTO UserProfile (user_id, bio, profile_picture_url)
VALUES (1, 'Software engineer at Birkini.', 'https://example.com/images/alice.jpg'),
       (2, 'Blockchain enthusiast.', 'https://example.com/images/bob.jpg');
