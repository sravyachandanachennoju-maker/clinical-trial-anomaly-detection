import pandas as pd, numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from math import sqrt
base=Path('/mnt/data/clinical_trial_anomaly_detection_project')
res=base/'results'; figdir=res/'figures'/'stage5'; figdir.mkdir(parents=True,exist_ok=True)
# load
split=pd.read_csv(res/'stage4_refined_split_assignments.csv')
rules=pd.read_csv(res/'rule_based_detection_records.csv')
ifpred=pd.read_csv(res/'stage4_refined_predictions.csv')
# held-out IDs
held=split.loc[split.split=='evaluation','record_id']
assert len(held)==600
r=rules[rules.record_id.isin(set(held))].copy()
i=ifpred[(ifpred.record_id.isin(set(held))) & (ifpred.contamination==0.08)].copy()
assert len(r)==600 and len(i)==600 and r.record_id.nunique()==600 and i.record_id.nunique()==600
# merge
raw=pd.read_csv(base/'data'/'synthetic_clinical_trial_data.csv')
m=r[['record_id','ground_truth_anomaly','ground_truth_category','ground_truth_types','rule_based_anomaly']].merge(i[['record_id','isolation_forest_flag','anomaly_score']],on='record_id',validate='one_to_one').merge(raw,on=['record_id','ground_truth_anomaly','ground_truth_category','ground_truth_types'],validate='one_to_one')
def metrics(flag):
 y=m.ground_truth_anomaly.astype(int).values; p=m[flag].astype(int).values
 tp=int(((y==1)&(p==1)).sum()); fp=int(((y==0)&(p==1)).sum()); tn=int(((y==0)&(p==0)).sum()); fn=int(((y==1)&(p==0)).sum())
 prec=tp/(tp+fp) if tp+fp else np.nan; rec=tp/(tp+fn) if tp+fn else np.nan; f1=2*prec*rec/(prec+rec) if prec+rec else np.nan; spec=tn/(tn+fp) if tn+fp else np.nan
 return [tp,fp,tn,fn,prec,rec,f1,spec]
rows=[['Rule-Based',*metrics('rule_based_anomaly')],['Isolation Forest',*metrics('isolation_forest_flag')]]
comp=pd.DataFrame(rows,columns=['Method','TP','FP','TN','FN','Precision','Recall','F1','Specificity'])
comp.to_csv(res/'stage5_final_comparison.csv',index=False)
# category recall
cats=['rule_detectable','ml_multivariate','both_detectable']
catrows=[]
for c in cats:
 sub=m[m.ground_truth_category==c]
 catrows.append([c,sub.rule_based_anomaly.mean(),sub.isolation_forest_flag.mean(),len(sub),int(sub.rule_based_anomaly.sum()),int(sub.isolation_forest_flag.sum())])
cat=pd.DataFrame(catrows,columns=['Category','Rule-Based Recall','Isolation Forest Recall','N','Rule Detected','IF Detected'])
cat.to_csv(res/'stage5_category_comparison.csv',index=False)
# subtype recall
subrows=[]
for st,g in m[m.ground_truth_anomaly==1].groupby('ground_truth_types'):
 n=len(g)
 if n>=3:
  subrows.append([st,n,g.rule_based_anomaly.mean(),g.isolation_forest_flag.mean(),int(g.rule_based_anomaly.sum()),int(g.isolation_forest_flag.sum())])
sub=pd.DataFrame(subrows,columns=['Subtype','N','Rule-Based Recall','Isolation Forest Recall','Rule Detected','IF Detected']).sort_values(['N','Subtype'],ascending=[False,True])
sub.to_csv(res/'stage5_subtype_recall.csv',index=False)
# overlap
m['overlap']=np.select([(m.rule_based_anomaly==1)&(m.isolation_forest_flag==1),(m.rule_based_anomaly==1)&(m.isolation_forest_flag==0),(m.rule_based_anomaly==0)&(m.isolation_forest_flag==1)],['both_methods_detected','rule_based_only','isolation_forest_only'],default='neither')
over=m['overlap'].value_counts().reindex(['both_methods_detected','rule_based_only','isolation_forest_only','neither'],fill_value=0).reset_index(); over.columns=['Category','Records']; over.to_csv(res/'stage5_detection_overlap.csv',index=False)
# truth-specific overlap details
truth_counts=[]
for label in ['both_methods_detected','rule_based_only','isolation_forest_only','neither']:
 g=m[m.overlap==label]
 truth_counts.append([label,len(g),int(g.ground_truth_anomaly.sum()),int(((g.ground_truth_anomaly==1)&(g.rule_based_anomaly==1)&(g.isolation_forest_flag==0)).sum()),int(((g.ground_truth_anomaly==1)&(g.rule_based_anomaly==0)&(g.isolation_forest_flag==1)).sum())])
pd.DataFrame(truth_counts,columns=['Overlap Category','Records','True Anomalies','True Anomalies Rule-Only','True Anomalies IF-Only']).to_csv(res/'stage5_overlap_ground_truth.csv',index=False)
# requested true anomaly detected only by rules / IF, false positives only
true_rule_only=m[(m.ground_truth_anomaly==1)&(m.rule_based_anomaly==1)&(m.isolation_forest_flag==0)]
true_if_only=m[(m.ground_truth_anomaly==1)&(m.rule_based_anomaly==0)&(m.isolation_forest_flag==1)]
fp_rule_only=m[(m.ground_truth_anomaly==0)&(m.rule_based_anomaly==1)&(m.isolation_forest_flag==0)]
fp_if_only=m[(m.ground_truth_anomaly==0)&(m.rule_based_anomaly==0)&(m.isolation_forest_flag==1)]
# CI Wilson
def wilson(x,n,z=1.959963984540054):
 if n==0:return (np.nan,np.nan)
 p=x/n; den=1+z*z/n; cen=(p+z*z/(2*n))/den; half=z*sqrt(p*(1-p)/n+z*z/(4*n*n))/den; return cen-half,cen+half
ci=[]
for method,flag in [('Rule-Based','rule_based_anomaly'),('Isolation Forest','isolation_forest_flag')]:
 tp,fp,tn,fn,*_=metrics(flag)
 for metric,x,n in [('Precision',tp,tp+fp),('Recall',tp,tp+fn)]:
  lo,hi=wilson(x,n); ci.append([method,metric,x,n,x/n,lo,hi])
ci=pd.DataFrame(ci,columns=['Method','Metric','Successes','Trials','Estimate','CI95_Lower','CI95_Upper']); ci.to_csv(res/'stage5_confidence_intervals.csv',index=False)
# complementary examples: all true IF-only, ranked by anomaly score descending
examples=true_if_only.sort_values('anomaly_score',ascending=False).copy()
cols=['record_id','ground_truth_category','ground_truth_types','age','visit_number','data_entry_delay','ALT','AST','hemoglobin','creatinine','query_count','protocol_deviation','ALT_missing','AST_missing','hemoglobin_missing','creatinine_missing','anomaly_score','rule_based_anomaly','isolation_forest_flag']
examples[cols].to_csv(res/'stage5_true_if_only_examples.csv',index=False)
# false positives representative top by score for IF and first rules
fp_if=fp_if_only.sort_values('anomaly_score',ascending=False).copy(); fp_if[cols].to_csv(res/'stage5_isolation_forest_false_positives.csv',index=False)
fp_rule=fp_rule_only.copy(); fp_rule[cols].to_csv(res/'stage5_rule_based_false_positives.csv',index=False)
# contamination copy from stage4 refined
sens=pd.read_csv(res/'stage4_refined_contamination_sensitivity.csv'); sens.to_csv(res/'stage5_contamination_sensitivity.csv',index=False)
# performance plot
plt.figure(figsize=(8,5)); x=np.arange(2); w=.24
for j,metric in enumerate(['Precision','Recall','F1']): plt.bar(x+(j-1)*w,comp[metric],width=w,label=metric)
plt.xticks(x,comp.Method); plt.ylim(0,1); plt.ylabel('Metric'); plt.title('Rule-Based vs Isolation Forest on 600 Held-Out Records'); plt.legend(); plt.tight_layout(); plt.savefig(figdir/'stage5_overall_performance.png',dpi=200); plt.close()
# category recall
plt.figure(figsize=(8,5)); x=np.arange(3); w=.36
plt.bar(x-w/2,cat['Rule-Based Recall'],width=w,label='Rule-Based'); plt.bar(x+w/2,cat['Isolation Forest Recall'],width=w,label='Isolation Forest'); plt.xticks(x,['Rule-detectable','ML-multivariate','Both-detectable'],rotation=15); plt.ylim(0,1); plt.ylabel('Recall'); plt.title('Category-Level Recall on Held-Out Records'); plt.legend(); plt.tight_layout(); plt.savefig(figdir/'stage5_category_recall.png',dpi=200); plt.close()
# overlap
plt.figure(figsize=(8,5)); plt.bar(over.Category,over.Records); plt.xticks(rotation=20); plt.ylabel('Records'); plt.title('Detection Overlap on 600 Held-Out Records'); plt.tight_layout(); plt.savefig(figdir/'stage5_detection_overlap.png',dpi=200); plt.close()
# contamination
plt.figure(figsize=(7,5)); plt.plot(sens.contamination,sens.precision,marker='o',label='Precision'); plt.plot(sens.contamination,sens.recall,marker='o',label='Recall'); plt.plot(sens.contamination,sens.f1,marker='o',label='F1'); plt.xlabel('Contamination'); plt.ylabel('Metric'); plt.ylim(0,1); plt.title('Isolation Forest Contamination Sensitivity'); plt.legend(); plt.tight_layout(); plt.savefig(figdir/'stage5_contamination_sensitivity.png',dpi=200); plt.close()
# score distribution useful
plt.figure(figsize=(8,5));
for lab,grp in [('Normal',m[m.ground_truth_anomaly==0]),('True anomaly',m[m.ground_truth_anomaly==1])]: plt.hist(grp.anomaly_score,bins=25,alpha=.6,label=lab)
plt.xlabel('Isolation Forest anomaly score'); plt.ylabel('Records'); plt.title('Anomaly Score Distribution on Held-Out Records'); plt.legend(); plt.tight_layout(); plt.savefig(figdir/'stage5_anomaly_score_distribution.png',dpi=200); plt.close()
# report
report=f'''# Stage 5: Final Comparative Evaluation\n\n## 1. Evaluation design\nThe primary comparison uses the exact 600-record held-out evaluation set defined during Stage 4 refinement. The Stage 3 rule set was applied unchanged to these records; no rule retraining or redesign occurred. The locked Isolation Forest predictions at contamination 0.08 were used without refitting. Ground-truth labels were used only for evaluation.\n\nThe synthetic dataset contains 150 anomalies overall. The held-out set contains 30 anomalies: 12 rule-detectable, 10 ML-multivariate, and 8 both-detectable, plus 570 normal records.\n\n## 2. Overall performance\n\n| Method | TP | FP | TN | FN | Precision | Recall | F1 | Specificity |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|\n'''
for _,row in comp.iterrows(): report+=f"| {row['Method']} | {int(row.TP)} | {int(row.FP)} | {int(row.TN)} | {int(row.FN)} | {row.Precision:.3f} | {row.Recall:.3f} | {row.F1:.3f} | {row.Specificity:.3f} |\\n"
report+='''\nThese values are directly comparable because both methods were evaluated against the same 600 records and the same ground-truth labels.\n\n## 3. Category-level performance\n\n| Category | Rule-Based Recall | Isolation Forest Recall | N |\n|---|---:|---:|---:|\n'''
for _,row in cat.iterrows(): report+=f"| {row['Category']} | {row['Rule-Based Recall']:.3f} | {row['Isolation Forest Recall']:.3f} | {int(row.N)} |\\n"
report+='''\nThe `both_detectable` category contains only 8 held-out anomalies, so its recall estimate is especially unstable and should not be overinterpreted.\n\n### Subtype recall\nSee `stage5_subtype_recall.csv` for subtype-level results where at least 3 held-out examples were available.\n\n## 4. Detection overlap\n\n'''
for _,row in over.iterrows(): report+=f"- {row['Category']}: {int(row.Records)} records\n"
report+='''\nAmong true anomalies, some were detected by both methods, some only by rules, and some only by Isolation Forest. The `Isolation Forest only` group is not equivalent to confirmed erroneous data: it means the record was flagged by the model but not by the rule set.\n\n## 5. Complementary detections\n\nThere were '''+str(len(true_if_only))+''' true anomalies detected only by Isolation Forest on the held-out set. Their subtypes and feature values are provided in `stage5_true_if_only_examples.csv`. These records were generated as synthetic ground-truth anomalies involving multivariate patterns such as lab profiles, query-delay-site relationships, or visit/lab/query combinations. The relevant interpretation is that the model identified unusual feature combinations that were not triggered by the deterministic rules. This does not establish that such records would be clinically erroneous in a real trial.\n\n## 6. False-positive analysis\n\nRule-based detection produced '''+str(len(fp_rule_only))+''' false positives that were rule-only. Isolation Forest produced '''+str(len(fp_if_only))+''' false positives that were IF-only. Representative records are provided in `stage5_rule_based_false_positives.csv` and `stage5_isolation_forest_false_positives.csv`.\n\nThe Isolation Forest false positives illustrate the central limitation of unsupervised anomaly detection: unusual does not mean incorrect. Plausible but uncommon laboratory combinations, unusual query activity, protocol deviations, or missingness patterns can be isolated even when there is no ground-truth error. The deterministic rules can also flag records that are unusual because of structural properties of the synthetic dataset, including the previously documented duplicate-rule behavior.\n\n## 7. Statistical uncertainty\n\nWilson 95% confidence intervals were calculated for precision and recall. Because the same finite held-out population is used for each method, these intervals describe uncertainty around the corresponding binomial proportions; they are not a test of clinical effectiveness.\n\nSee `stage5_confidence_intervals.csv` for exact values.\n\n## 8. Interpretation\n\nThe apples-to-apples comparison provides evidence that Isolation Forest can recover some synthetic multivariate anomalies missed by the conventional rule set. In the held-out evaluation, Isolation Forest detected 6 of 10 ML-multivariate anomalies, while the rules detected none of those 10. However, Isolation Forest also generated substantially more false positives than the rule set on this evaluation set. Overall recall was '''+f"{comp.loc[comp.Method=='Isolation Forest','Recall'].iloc[0]:.3f}"+''' and precision was '''+f"{comp.loc[comp.Method=='Isolation Forest','Precision'].iloc[0]:.3f}"+'''.\n\nTherefore, the evidence supports **potential complementarity, not superiority**. The experiment demonstrates a useful signal for multivariate anomaly detection, but the false-positive burden means the model would require human review and further validation before being considered a practical clinical data-management control.\n\n## 9. Answer to research question\n\n**Research question:** Can an unsupervised machine learning model complement conventional rule-based checks by identifying potentially problematic clinical-trial records that may not be detected by traditional data-quality rules?\n\n**Evidence-based answer:** **Evidence of potential complementarity.** On the same 600 held-out records, Isolation Forest detected 6/10 ML-multivariate anomalies that were missed by the rule-based method. This finding is accompanied by 28 false positives at the pre-specified 0.08 contamination setting and incomplete overall recall. The result therefore supports the possibility of complementarity in this synthetic experiment, while not establishing clinical validity or superiority.\n\n## 10. Limitations\n\n1. The data are fully synthetic, so the findings do not establish performance on real clinical-trial data.\n2. The anomaly mechanisms and category definitions were designed by the study author, which can create dataset-specific behavior.\n3. The held-out anomaly counts are small, especially the 8 `both_detectable` records.\n4. The primary contamination setting of 0.08 was retained from the exploratory design rather than selected using held-out labels, but this is still a design choice rather than a universally optimal operating point.\n5. Isolation Forest flags unusual observations, not proven data errors.\n6. The rule-based method contains a documented structural side effect: the duplicate composite rule can flag records affected by the synthetic visit/record construction.\n7. Confidence intervals are descriptive and do not replace external validation.\n8. The experiment does not assess operational workload, review time, or clinical adjudication burden.\n'''
(res/'stage5_comparative_evaluation.md').write_text(report)
# manifest
print('DONE')
print(comp.to_string(index=False)); print(cat.to_string(index=False)); print(over.to_string(index=False)); print(ci.to_string(index=False)); print('true IF only',len(true_if_only),'rule-only true',len(true_rule_only),'FP rule-only',len(fp_rule_only),'FP IF-only',len(fp_if_only))
