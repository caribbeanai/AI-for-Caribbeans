# Lesson 3, Anomaly detection

Find the unusual. Fraud, equipment failure, illegal fishing, suspicious login.

## Approaches

- Statistical: z-score, modified z-score, IQR.
- Distance based: nearest neighbour distance.
- Model based: Isolation Forest, One-Class SVM, autoencoders.
- Time series: residuals from a forecast, change point detection.

## Caribbean examples

- Spike in remittance volume from a single sender during a hurricane month: investigate, not suspect.
- A cruise ship arrival pattern that breaks the schedule: maintenance issue or weather event.
- An unusual rainfall reading from a single weather station: sensor fault, or local microclimate.

## Practical tip

Anomaly does not mean fraud. It means uncommon. Always validate with a domain expert before acting.
