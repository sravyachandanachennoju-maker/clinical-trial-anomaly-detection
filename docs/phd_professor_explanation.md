# Explaining the Project to a PhD Professor

## 30-second explanation

> I built a controlled synthetic clinical-trial data-quality experiment to test whether an unsupervised anomaly detector could complement conventional deterministic checks. I generated 3,000 synthetic records with predefined anomaly mechanisms, kept the ground-truth labels out of model features and training targets, and compared the rule-based detector with Isolation Forest on the same 600-record held-out set. The rules performed better overall, but detected none of the 10 ML-multivariate anomalies, while Isolation Forest detected 6. The ML method also produced 28 false positives. So I am not claiming that ML replaces rules. I am testing whether it can add a second layer of signals for multivariate patterns that predefined checks may miss.

## 60-second explanation

> My research question was whether unsupervised anomaly detection can complement conventional clinical data-quality rules. I created a fully synthetic dataset of 3,000 clinical-trial-like records across 10 synthetic sites and injected 150 known anomalies into three categories: rule-detectable, ML-multivariate, and both-detectable. I first applied 11 deterministic rules. Then I trained an Isolation Forest using 14 numerical and binary features, with 300 trees and a fixed random seed. Preprocessing was fitted only on the 2,400-record training set, and the final comparison was performed on 600 held-out records. Overall, the rule-based method had 90.9% precision and 66.7% recall, while Isolation Forest had 33.3% precision and 46.7% recall. The interesting result was category-specific: Isolation Forest detected 6 of 10 ML-multivariate anomalies that the rules did not detect. That came with 28 false positives, so the result points to potential complementarity rather than superiority.

## 3-minute technical explanation

> I designed the experiment around a simple clinical data-management problem: deterministic edit checks are interpretable and operationally useful, but they only detect conditions that have been explicitly encoded. I wanted to test whether an unsupervised model could identify unusual combinations of otherwise plausible variables.
>
> The dataset contains 3,000 synthetic records, 10 sites, visits 1 through 5, and 150 injected anomalies. The anomaly categories were deliberately separated so that I could distinguish explicit rule-detectable problems from multivariate patterns. Ground truth was created during data generation, but it was not given to Isolation Forest as a feature or target. The final evaluation used a stratified 80/20 split, with 2,400 training records and 600 held-out records.
>
> The deterministic detector used 11 rules covering missing required labs, extreme laboratory values, timing inconsistencies, excessive entry delay, invalid visits, duplicate composite records, and a joint ALT/AST condition. Isolation Forest used age, visit number, entry delay, four laboratory values, query count, protocol deviation, four missingness indicators, and an ALT/AST ratio. Identifiers, site ID, raw dates, and all ground-truth fields were excluded.
>
> I fitted median imputation and standardization only on the training set. Isolation Forest used 300 trees, random seed 20260924, and a pre-specified contamination of 0.08. I also examined 0.05 and 0.10 as sensitivity settings. The primary setting was not selected after looking at held-out F1.
>
> On the same 600 held-out records, rules produced 20 true positives, 2 false positives, 568 true negatives, and 10 false negatives. Isolation Forest produced 14 true positives, 28 false positives, 542 true negatives, and 16 false negatives. This gave precision/recall of 90.9%/66.7% for rules and 33.3%/46.7% for Isolation Forest.
>
> The main scientific point is not that the ML model was better. It was not better overall in this experiment. The useful observation is that the methods detected different kinds of synthetic anomalies. Rules detected 12/12 rule-detectable and 8/8 both-detectable held-out anomalies, but 0/10 ML-multivariate anomalies. Isolation Forest detected 6/10 ML-multivariate anomalies. At the same time, the model produced 28 false positives. Therefore, an ML flag should be interpreted as a potential data-quality signal that requires review, not as a confirmed error.

## Why did you choose this research question?

I chose it because it connects a practical clinical data-management problem with a manageable methodological question. In clinical data management, deterministic checks are essential, but they encode predefined expectations. I wanted to test, in a controlled environment, whether an unsupervised method could add information about combinations of variables that are difficult to express as individual rules.

## Why compare rules with Isolation Forest?

The comparison creates a clear baseline. If Isolation Forest is used without a conventional reference, it is difficult to know whether its flags add information or simply generate more alerts. The rule-based system represents an interpretable deterministic layer, while Isolation Forest represents an unsupervised multivariate layer.

## Why was Isolation Forest not expected to replace rules?

Isolation Forest detects unusual observations in feature space. It does not know whether an unusual observation is an actual data error, a legitimate clinical value, a site-specific operational pattern, or an artifact of the synthetic generator. Deterministic rules remain valuable because their logic can be explicitly defined, reviewed, and linked to known data-quality requirements.

## What did you actually discover?

On the primary held-out comparison, rules had higher overall precision and recall. The complementary finding was that Isolation Forest detected 6 of 10 ML-multivariate anomalies that the rule-based detector missed. The model therefore recovered some synthetic multivariate signals outside the deterministic rule set, but detection was incomplete.

## Why are the false positives important?

The 28 Isolation Forest false positives are central to the interpretation. An anomaly detector is designed to find unusual observations, not to prove that an observation is wrong. In a real workflow, every additional alert can create review work. A method that identifies more unusual records but generates many non-actionable alerts may not improve the operational process. That is why precision, reviewer adjudication, and workload need to be studied together in the next phase.

## What are the major limitations?

The biggest limitations are the synthetic dataset, injected rather than clinically adjudicated anomalies, the small number of held-out anomalies, the synthetic assumptions used to construct multivariate patterns, the Isolation Forest false-positive burden, the lack of external validation, and the absence of prospective workflow evaluation. The training set also retained synthetic anomalies because removing them with ground-truth labels would change the unsupervised learning problem. Finally, the duplicate rule has a documented structural side effect in the synthetic construction.

## What would you do with real clinical-trial data?

I would move to appropriately de-identified clinical-trial data under the relevant governance and data-use permissions. I would define anomaly adjudication with experienced clinical data managers and subject-matter experts, preserve a strict separation between training and evaluation data, and examine temporal and site-level context. I would measure not only detection performance but also reviewer workload, alert acceptance, time to resolution, reproducibility, and the stability of signals across studies.

I would also avoid assuming that a synthetic ground-truth label maps directly to a real-world clinical error. Real-data validation would require an explicit adjudication process.

## What would the next experiment be?

The next experiment would be a prospective or retrospective evaluation on de-identified real clinical-trial data with human adjudication. I would compare Isolation Forest with additional unsupervised methods, evaluate explainable feature-level contributions to each alert, test temporal and site-context features, and measure the trade-off between additional anomaly discovery and review burden. The goal would be to determine whether a second-layer anomaly detector adds actionable information beyond existing data-quality controls.

## Phrases to use

- synthetic ground-truth anomaly
- algorithmic anomaly flag
- potential data-quality signal
- potential complementarity
- requires human review
- controlled methodological experiment

## Phrases to avoid

- AI is better than traditional clinical data management
- the model detects clinical errors
- clinically validated
- ready for clinical deployment
- Isolation Forest is novel
- ML proved it improves clinical trials
