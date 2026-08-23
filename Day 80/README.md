# Day 80 – The Tragic Discovery of Handwashing 🧼📊

## Overview

Day 80 mein hum **Dr. Ignaz Semmelweis** ki tragic lekin groundbreaking medical discovery ko data science ke perspective se analyze karte hain.

1840s mein Vienna General Hospital mein doctors ke ward mein childbirth ke baad hone wali **puerperal (childbed) fever** ki death rate bohat high thi. Semmelweis ne observe kiya ke doctors aur medical students autopsies ke baad directly maternity ward mein patients ko examine karte thay.

Unhon ne suggest kiya ke doctors apne hands ko **chlorinated lime solution** se wash karein.

Handwashing introduce hone ke baad mortality rate dramatically decrease hui.

Is project mein hum historical pattern ko data ke through investigate karte hain aur **independent two-sample t-test** use karke determine karte hain ke dono groups ke mortality rates mein statistically significant difference hai ya nahi.

---

## 🎯 Learning Objectives

Is project ke end tak hum seekhte hain:

* Historical data ko Data Science problem mein convert karna
* Distributions ko visualize karna
* Mean aur variation ko understand karna
* Before vs After intervention compare karna
* Independent two-sample t-test perform karna
* Null aur alternative hypothesis samajhna
* p-value interpret karna
* Statistical significance determine karna
* Data visualization ke through evidence communicate karna

---

## 📚 Historical Context

Dr. Ignaz Semmelweis ne observe kiya ke **Doctor's Clinic** mein maternal mortality rate **Midwife's Clinic** ke muqable mein significantly higher thi.

Unhon ne suspect kiya ke doctors ke hands par autopsy material transfer hone ki wajah se infections spread ho rahe thay.

1847 mein handwashing protocol introduce kiya gaya.

Result:

**Mortality rate mein dramatic decrease.**

Ye discovery us waqt widely accept nahi hui aur Semmelweis ko apni life mein proper recognition nahi mili.

Isi wajah se is story ko aksar **"Tragic Discovery of Handwashing"** kaha jata hai.

---

## 🧪 Statistical Experiment

Hum do groups compare karte hain:

### Before Handwashing

Doctors ke handwashing protocol introduce hone se pehle mortality rates.

### After Handwashing

Handwashing protocol implement hone ke baad mortality rates.

Humara main question:

> Kya handwashing ke baad mortality rate statistically significantly decrease hui?

---

## 📊 Distributions

Sirf average compare karna enough nahi hota.

Hum distributions ko visualize karke dekhte hain:

* Data kis range mein spread hai?
* Mean kahan located hai?
* Variation kitni hai?
* Dono groups overlap karte hain ya separate hain?
* Intervention ke baad distribution kis direction mein shift hui?

Useful visualizations include:

* Histogram
* KDE distribution
* Box plot
* Mean comparison
* Before vs After distribution

---

## 🧮 Independent Two-Sample T-Test

Do independent groups ke means compare karne ke liye hum **independent t-test** use karte hain.

### Null Hypothesis (H₀)

There is **no significant difference** between the mean mortality rates before and after handwashing.

### Alternative Hypothesis (H₁)

There **is a significant difference** between the mean mortality rates before and after handwashing.

Hum significance level:

```text
α = 0.05
```

use karte hain.

### Decision Rule

Agar:

```text
p-value < 0.05
```

to hum **Null Hypothesis reject** karte hain.

Agar:

```text
p-value >= 0.05
```

to hum Null Hypothesis reject nahi karte.

---

## 🔬 Python Implementation

Statistical test perform karne ke liye:

```python
from scipy.stats import ttest_ind

t_stat, p_value = ttest_ind(
    before,
    after,
    equal_var=False
)

print("T-statistic:", t_stat)
print("P-value:", p_value)
```

`equal_var=False` Welch's t-test perform karta hai, jo unequal variances ki situation mein useful hota hai.

---

## 📈 Visualization

Distribution visualize karne ke liye:

```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.histplot(before, kde=True, label="Before Handwashing")
sns.histplot(after, kde=True, label="After Handwashing")

plt.legend()
plt.title("Mortality Rate Distribution")
plt.show()
```

Box plot se dono distributions ka comparison aur clear hota hai:

```python
sns.boxplot(data=[before, after])
plt.title("Before vs After Handwashing")
plt.show()
```

---

## 🔍 What We Learn From The Analysis

Analysis ka main purpose sirf ye show karna nahi hai ke average mortality decrease hui.

Hum statistical evidence use karte hain to determine whether the observed difference is likely to be meaningful rather than simply random variation.

A significant t-test result provides evidence that the two groups have different mean mortality rates.

---

## 🧠 Key Concepts Covered

| Concept            | What We Learn                    |
| ------------------ | -------------------------------- |
| Distribution       | Data ka spread aur shape         |
| Mean               | Central tendency                 |
| Standard deviation | Data ki variation                |
| Histogram          | Distribution visualize karna     |
| KDE                | Smooth probability distribution  |
| Box plot           | Median, spread aur outliers      |
| T-test             | Do means compare karna           |
| T-statistic        | Difference relative to variation |
| P-value            | Statistical evidence             |
| Hypothesis testing | Data-driven decision making      |
| Significance level | `α = 0.05` decision threshold    |

---

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* SciPy
* Seaborn
* Matplotlib

---

## ▶️ How to Run

Install required libraries:

```bash
pip install pandas numpy scipy seaborn matplotlib
```

Run the analysis:

```bash
python semmelweis_analysis.py
```

---

## 💡 Key Takeaways

### 1. Visualization comes before statistics

Distribution ko visualize karne se data ka structure samajhne mein help milti hai.

### 2. Mean alone is not enough

Do groups ka mean similar ya different ho sakta hai, lekin distribution aur variation bhi important hain.

### 3. T-test gives statistical evidence

T-test humein batata hai ke observed difference statistically significant hai ya nahi.

### 4. P-value ko correctly interpret karein

Small p-value ka matlab ye nahi ke "probability that the hypothesis is false" hai.

Ye evidence provide karta hai against the null hypothesis.

### 5. Data can reveal important truths

Semmelweis ka observation ek powerful example hai ke careful observation + data analysis medical practice ko transform kar sakta hai.

---

## 🏆 Day 80 Challenge

Try these experiments:

1. Before aur after distributions ko separately plot karein.
2. Mean aur median compare karein.
3. Box plot mein outliers identify karein.
4. T-test ka `p-value` change hota hai ya nahi jab sample size increase hota hai?
5. Different significance levels (`0.01`, `0.05`, `0.10`) ke results compare karein.
6. Welch's t-test aur standard independent t-test ke results compare karein.

---

## 🚀 Final Thought

The story of Semmelweis teaches an important Data Science lesson:

> **Observation can raise a question, but data and statistical analysis can provide evidence.**

Day 80 mein humne sirf ek historical event study nahi kiya — humne dekha ke **distributions, visualization aur hypothesis testing** real-world problems ko scientifically investigate karne mein kaise use hote hain.

**Day 80 Complete! 🎉**
