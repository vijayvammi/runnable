from examples.tutorials.steps import clean, extract_text, model_fit, tfidf, tokenize
from runnable import Pipeline, PythonTask, pickled


def driver():
    x, labels = extract_text(
        url="https://raw.githubusercontent.com/axsauze/reddit-classification-exploration/master/data/reddit_train.csv",
        encoding="ISO-8859-1",
        features_column="BODY",
        labels_column="REMOVED",
    )

    cleaned_x = clean(x)
    tokenised_x = tokenize(cleaned_x)
    vectorised_x = tfidf(tokenised_x, max_features=1000, ngram_range=3)
    y_probabilities = model_fit(vectorised_x, labels, c_param=0.1)

    print(y_probabilities)


def runnable_pipeline():
    extract_task = PythonTask(name="extract", function=extract_text, returns=[pickled("x"), pickled("labels")])
    clean_task = PythonTask(name="clean", function=clean, returns=[pickled("cleaned_x")])
    tokenize_task = PythonTask(name="tokenize", function=tokenize, returns=[pickled("tokenised_x")])
    vectorise_task = PythonTask(name="tfidf", function=tfidf, returns=[pickled("vectorised_x")])

    model_fit_task = PythonTask(
        name="model_fit",
        function=model_fit,
        returns=[pickled("y_probabilities")],
        terminate_with_success=True,
    )

    extract_task >> clean_task >> tokenize_task >> vectorise_task >> model_fit_task

    pipeline = Pipeline(
        start_at=extract_task,
        steps=[extract_task, clean_task, tokenize_task, vectorise_task, model_fit_task],
        add_terminal_nodes=True,
    )

    pipeline.execute(parameters_file="examples/tutorials/parameters.yaml")

    return pipeline


if __name__ == "__main__":
    # driver()
    runnable_pipeline()
