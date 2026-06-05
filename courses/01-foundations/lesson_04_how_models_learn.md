# Lesson 4, How models learn

Most ML follows the same loop.

1. **Get data.** Lots of examples.
2. **Pick a model.** Linear regression, decision tree, neural network, etc.
3. **Define a loss.** A number that says how wrong the model is.
4. **Train.** Adjust the model's parameters to reduce the loss.
5. **Evaluate.** Check on data the model has not seen.
6. **Iterate.** Try a different model, add features, clean the data, repeat.

## A concrete picture

You want to predict the price of a 2 bedroom apartment in New Kingston.

Features: square footage, distance from Half Way Tree, year built, number of bathrooms, security yes or no.
Label: rent in JMD per month.

You collect 1,000 listings. You train a regression model. The model says: every extra square foot adds about JMD 95 to monthly rent, after holding other features constant.

You test on 200 listings the model has not seen. Average error is JMD 8,000. Decision: is that good enough for your use case?

## Overfitting, the most common mistake

A model that memorises the training data but fails on new data is overfitting. Like a student who memorises past papers but cannot solve a new question. Defences:

- Hold out a test set you never train on.
- Use cross validation.
- Keep the model simpler than you think you need.
- Add more data.

## Underfitting

The opposite. The model is too simple to capture the pattern. Often shows up as poor performance on both training and test data.

## The bias variance trade off

Simple models miss patterns (high bias). Complex models chase noise (high variance). The art is finding the middle. Plotting training error against test error as the model grows tells the story.
