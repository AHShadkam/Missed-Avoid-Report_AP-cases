WITH avoid_ui AS
(
  SELECT service_timestamp,
          domain_name,
          LOWER(symptom) symptom,
          case_data 
   FROM ad.log_avoid_ui
   WHERE service_timestamp >= CURRENT_DATE-37
   AND len(case_data) !=0 
),


popular_missed_avoids AS
(
    SELECT 
        som.dm_nm AS domain_name,
        LOWER(aps.symptom) AS symptom, 
        count(1) AS frequency
    FROM ad.so_main som
        INNER JOIN ad.cib_session cib using (so_key)
        LEFT JOIN ad.so_jc soj USING (so_key)
        LEFT JOIN src.sstxtjc sstxtjc ON (soj.pri_job_cd=sstxtjc.job_cd AND soj.pri_job_cd_crg_cd = sstxtjc.job_cd_crg_cd AND som.mds_sp_cd = sstxtjc.sp_cd)
        LEFT JOIN ad.log_ap_summary aps USING (so_key)
    WHERE sstxtjc.job_cd_cat_cd = 'CI' 
      AND som.so_py_met_cd IN ('IW','SP')
      AND som.so_crt_dt BETWEEN CURRENT_DATE-37 AND CURRENT_DATE-7
      AND aps.ap_call_cnt >=1
      AND aps.case_count > 0
    GROUP BY 
          som.dm_nm,
          LOWER(aps.symptom)
    ORDER BY count(1) DESC
    LIMIT 100
)


SELECT T1.domain,
	   T1.symptom,
       popular_missed_avoids.frequency AS Missed_Avoid_freq,
       T1.svc_ts,
       avoid_ui.case_data
FROM
(select max(aui.service_timestamp) AS svc_ts,
	   aui.domain_name AS domain,
       aui.symptom AS symptom
from avoid_ui AS aui inner join popular_missed_avoids pma
ON (aui.domain_name=pma.domain_name AND aui.symptom=pma.symptom)
GROUP BY aui.domain_name,aui.symptom ) AS T1
INNER JOIN avoid_ui ON (T1.svc_ts=avoid_ui.service_timestamp AND T1.domain=avoid_ui.domain_name AND T1.symptom=avoid_ui.symptom)
INNER JOIN popular_missed_avoids ON (T1.domain=popular_missed_avoids.domain_name AND T1.symptom=popular_missed_avoids.symptom)
ORDER BY popular_missed_avoids.frequency DESC;
