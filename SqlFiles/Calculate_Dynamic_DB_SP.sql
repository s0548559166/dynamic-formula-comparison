CREATE OR ALTER PROCEDURE dbo.Calculate_Dynamic_DB_SP
AS
BEGIN
    SET NOCOUNT ON; 

    DECLARE @TargilID INT;
    DECLARE @FormulaMain NVARCHAR(MAX);
    DECLARE @Tnai NVARCHAR(MAX);
    DECLARE @FormulaFalse NVARCHAR(MAX); 
    
    DECLARE @DynamicSQL NVARCHAR(MAX);
    DECLARE @StartTime DATETIME2;
    DECLARE @RunTime FLOAT;
    DECLARE @MethodName VARCHAR(50) = 'DB_SP'; 
    
    DECLARE targil_cursor CURSOR LOCAL FAST_FORWARD FOR
    SELECT targil_id, targil, tnai, false_targil 
    FROM dbo.t_targil; 

    OPEN targil_cursor;
    
    FETCH NEXT FROM targil_cursor INTO @TargilID, @FormulaMain, @Tnai, @FormulaFalse;

    WHILE @@FETCH_STATUS = 0
    BEGIN
        SET @StartTime = GETDATE(); 
        
        DECLARE @CalcExpression NVARCHAR(MAX);
        
        IF @Tnai IS NULL OR LTRIM(RTRIM(@Tnai)) = '' 
        BEGIN
            SET @CalcExpression = @FormulaMain;
        END
        ELSE
        BEGIN
            SET @CalcExpression = 
                'CASE WHEN (' + @Tnai + ') THEN (' + @FormulaMain + ') ELSE (' + @FormulaFalse + ') END';
        END

        SET @DynamicSQL = 
        N'
        INSERT INTO dbo.t_results (data_id, targil_id, method, result)
        SELECT 
            data_id, 
            ' + CAST(@TargilID AS VARCHAR(10)) + ', 
            ''' + @MethodName + ''',
            CAST((' + @CalcExpression + ') AS FLOAT) AS Calculated_Result
        FROM dbo.t_data; 
        ';

        EXEC sp_executesql @DynamicSQL;

        SET @RunTime = DATEDIFF(ms, @StartTime, GETDATE()) / 1000.0; 
        
        INSERT INTO dbo.t_log (targil_id, method, time_run)
        VALUES (@TargilID, @MethodName, @RunTime);

        FETCH NEXT FROM targil_cursor INTO @TargilID, @FormulaMain, @Tnai, @FormulaFalse;
    END

    CLOSE targil_cursor;
    DEALLOCATE targil_cursor;
END
GO