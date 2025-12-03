use master
go
create  database Ex 
use Ex

CREATE TABLE dbo.t_data (
    data_id INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    a FLOAT NOT NULL,
    b FLOAT NOT NULL,
    c FLOAT NOT NULL,
    d FLOAT NOT NULL
);

CREATE TABLE dbo.t_targil (
    targil_id INT IDENTITY(1,1) PRIMARY KEY NOT NULL, 
    targil NVARCHAR(MAX) NOT NULL,
    tnai NVARCHAR(MAX) NULL,          
    false_targil NVARCHAR(MAX) NULL
);

CREATE TABLE dbo.t_results (
    resultsl_id INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    targil_id INT NOT NULL,
    data_id INT NOT NULL,
    method VARCHAR(50) NOT NULL,
    result FLOAT,
    CONSTRAINT FK_t_results_targil FOREIGN KEY (targil_id)
        REFERENCES dbo.t_targil (targil_id)
        ON DELETE CASCADE,
    CONSTRAINT FK_t_results_data FOREIGN KEY (data_id)
        REFERENCES dbo.t_data (data_id)
        ON DELETE CASCADE
);

CREATE TABLE dbo.t_log (
    log_id INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    targil_id INT NOT NULL,
    method VARCHAR(50) NOT NULL,
    time_run FLOAT, 
    CONSTRAINT FK_t_log_targil FOREIGN KEY (targil_id)
        REFERENCES dbo.t_targil (targil_id)
        ON DELETE CASCADE
);
GO