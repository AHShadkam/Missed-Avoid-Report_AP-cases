SELECT Kai_prj_nm,
         Kai_srh_tms, 
         Kai_sln_id
FROM ad.cib_session
WHERE Avd_7d_stick = TRUE
AND len(Kai_sln_id) !=0
AND date(ses_sta_ts) BETWEEN '2016-04-10' AND '2016-08-10'
