DROP MATERIALIZED VIEW IF EXISTS avg_hpf_scores;
DROP MATERIALIZED VIEW IF EXISTS lexmapr_iri;

CREATE  MATERIALIZED VIEW  lexmapr_iri as SELECT fdc_id, "Product_Desc" as product_desc, "Matched_Components" as matched_components, "Match_Status" as match_status,
       case when "Match_Status" = 'Full Term Match' then 1 else 0 end as match_id,
       unnest(regexp_matches("Matched_Components", '(?<=:)(.*?)(?=,\s|$)', 'g')) as component_iri
FROM "LexMaprMapping_Products";

CREATE MATERIALIZED VIEW  avg_hpf_scores as SELECT
    fdc_list.matched_components,
    COUNT(matched_components) AS n,
    AVG(case when fsod = 'True' then 1 else 0 end +
    case when fs = 'True' then 1 else 0 end +
    case when csod = 'True' then 1 else 0 end) AS hpf_score
FROM usda_2022_hpf_component as hpf inner join lexmapr_iri As fdc_list
    ON fdc_list.fdc_id = hpf.fdc_id
GROUP BY matched_components
ORDER BY hpf_score;

-- Hot dog query example
WITH fdc_list as
    (SELECT DISTINCT fdc_id, matched_components, product_desc
    FROM lexmapr_iri
--     WHERE match_status = 'Full Term Match' AND
    WHERE match_id = 1 AND
        component_iri = any(array['FOODON_00001009','FOODON_03302012','FOODON_03311509','FOODON_03310934','FOODON_03310577','FOODON_03310576','FOODON_03310165','FOODON_03310164','FOODON_03310163','FOODON_03310162','FOODON_03307230','FOODON_00001605','FOODON_00004095','FOODON_00003924','FOODON_00003288','FOODON_00003890','FOODON_00001224']))
, hpf_fdc_list AS (SELECT DISTINCT ON (fdc_list.matched_components)
    fdc_list.matched_components,
    fdc_list.product_desc,
    hpf.n,
    hpf.hpf_score
FROM fdc_list INNER JOIN avg_hpf_scores as hpf
    ON fdc_list.matched_components = hpf.matched_components)
SELECT ROW_NUMBER() OVER (ORDER BY hpf_score ASC) AS rank, *
From hpf_fdc_list
ORDER BY rank;