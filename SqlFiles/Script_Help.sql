--סקריפט השוואה--
SELECT 
    COUNT(*) AS Differences_Count
FROM t_results R_AST
JOIN t_results R_DB 
  ON R_AST.data_id = R_DB.data_id 
  AND R_AST.targil_id = R_DB.targil_id
WHERE R_AST.method = 'safe_ast' 
  AND R_DB.method = 'DB_SP'
  AND ABS(R_AST.result - R_DB.result) > 0.0001; 


  --שאילתה עזר להצגת נתונים לדו"ח ההשוואה בין שתי השיטות--
  SELECT 
    method,
    COUNT(*) AS Total_Formulas_Run,
    SUM(time_run) AS Total_Run_Time_Seconds,
    AVG(time_run) AS Average_Run_Time_Seconds,
    MIN(time_run) AS Min_Run_Time_Seconds,
    MAX(time_run) AS Max_Run_Time_Seconds
FROM t_log
GROUP BY method;

