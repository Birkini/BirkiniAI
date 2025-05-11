-- Create and select the Birkini database
CREATE DATABASE IF NOT EXISTS birkini;
USE birkini;

-- Table: Users
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active'
);

-- Table: Transactions
CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_type ENUM('deposit', 'withdrawal', 'transfer') NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'completed', 'failed') DEFAULT 'pending',
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Table: Backups
CREATE TABLE Backups (
    backup_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    backup_type ENUM('full', 'incremental') NOT NULL,
    file_location VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('completed', 'failed') DEFAULT 'completed',
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Table: AuditLogs
CREATE TABLE AuditLogs (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(255) NOT NULL,
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(50),
    status ENUM('success', 'failure') DEFAULT 'success',
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Table: SystemSettings
CREATE TABLE SystemSettings (
    setting_id INT AUTO_INCREMENT PRIMARY KEY,
    setting_name VARCHAR(100) NOT NULL UNIQUE,
    setting_value TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table: APIRateLimits
CREATE TABLE APIRateLimits (
    rate_limit_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    requests_made INT DEFAULT 0,
    last_reset TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Table: UserProfile
CREATE TABLE UserProfile (
    profile_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    bio TEXT,
    profile_picture_url VARCHAR(255),
    social_links JSON,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Sample Data: Users
INSERT INTO Users (username, email, password_hash, status) VALUES
    ('alice', 'alice@example.com', 'hashed_password_123', 'active'),
    ('bob', 'bob@example.com', 'hashed_password_456', 'active');

-- Sample Data: Transactions
INSERT INTO Transactions (user_id, amount, transaction_type, status) VALUES
    (1, 100.00, 'deposit', 'completed'),
    (2, 50.50, 'withdrawal', 'completed');

-- Sample Data: Backups
INSERT INTO Backups (user_id, backup_type, file_location) VALUES
    (1, 'full', '/backups/backup_2023_01_01.zip'),
    (2, 'incremental', '/backups/backup_2023_01_02.zip');

-- Sample Data: AuditLogs
INSERT INTO AuditLogs (user_id, action, ip_address, status) VALUES
    (1, 'login', '192.168.1.1', 'success'),
    (2, 'file upload', '192.168.1.2', 'failure');

-- Sample Data: SystemSettings
INSERT INTO SystemSettings (setting_name, setting_value) VALUES
    ('max_file_upload_size', '50MB'),
    ('default_language', 'English');

-- Sample Data: APIRateLimits
INSERT INTO APIRateLimits (user_id, requests_made) VALUES
    (1, 50),
    (2, 10);

-- Sample Data: UserProfile
INSERT INTO UserProfile (user_id, bio, profile_picture_url) VALUES
    (1, 'Software engineer at Birkini.', 'https://example.com/images/alice.jpg'),
    (2, 'Blockchain enthusiast.', 'https://example.com/images/bob.jpg');
