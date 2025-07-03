

## 📩 Problem:

Humein predict karna hai ke **koi email spam hai ya nahi (1 ya 0)**.

---

## ✅ Step-by-Step Breakdown:

### 🧾 1. **Dataset**

Tumhara dataset emails ka hai jisme columns hain:

* `Subject`, `Sender`, `ContentLength`, `NumLinks`, `IsSpam`
* `IsSpam` → Yeh **target** hai (jisko predict karna hai)

---

### 🧼 2. **Data Splitting**

Dataset ko do parts mein divide karte hain:

```python
X = data[['Sender']]         # Features (jo model ko dete ho)
y = data['IsSpam']           # Labels (jo model ko sikhate ho)

X_train, X_test, y_train, y_test = train_test_split(X, y)
```

---

### 🔤 3. **Text Conversion (Vectorization)**

Computer **text ko directly samajh nahi sakta**, is liye hum `"Sender"` jaise text data ko **numbers** mein badalte hain:

```python
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train['Sender'])
X_test_vec = vectorizer.transform(X_test['Sender'])
```

🧠 Ab model ko numeric values mil gayi hain — har sender email ko numbers (features) mein badal diya gaya.

---

### 🧠 4. **Model Training**

Ab machine learning model (Naive Bayes) ko train karte hain:

```python
model = MultinomialNB()
model.fit(X_train_vec, y_train)
```

Yeh model ab seekh gaya ke kaun se "Sender" spam bhejta hai aur kaun nahi.

---

### 🧪 5. **Prediction**

Ab model test emails par predict karta hai:

```python
y_pred = model.predict(X_test_vec)
```

Aur tumhe output milta hai:

```
[0 0 1 0 1 0 0 0 0 1 0 0 1 1 1 1 1 1 0 1]
```

---

## 🔚 Summary:

| Step      | Kya ho raha hai?                       |
| --------- | -------------------------------------- |
| Dataset   | Email data load                        |
| Split     | Training aur testing parts mein divide |
| Vectorize | Text data (Sender) → Numbers           |
| Train     | Naive Bayes model seekhta hai patterns |
| Predict   | Model test data pe predict karta hai   |

---



