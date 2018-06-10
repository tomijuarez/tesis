#!/bin/bash

ROOT_PATH=$(cd ../../ && pwd)
TOOLS_PATH=$ROOT_PATH/tools
SMARTWEB_PATH=$ROOT_PATH/isistan-smartweb/isistan/smartweb/core/SmartWebServer.py
STANDFORD_ROOT_PATH=$ROOT_PATH/dependencies/stanford-ner-2015-04-20
STANFORD_NER_PATH=$STANDFORD_ROOT_PATH/stanford-ner.jar
DATASET_PATH=$ROOT_PATH/datasets
SMARTWEB_PORT=8081
STANFORD_NER_PORT=8080
SLEEP_TIME=10s
export PYTHONPATH=$PYTHONPATH:$ROOT_PATH/isistan-smartweb/

RESULTS_PROCESSOR_PATH=$TOOLS_PATH/results_processor/results_processor.py

HITLIST_FILE_PATH=hitlist.xml
QUERY_FILE_PATH=queries.csv
MASHAPE_DATASET_PATH=$DATASET_PATH/mashape_dataset/

run_kmeans=false
run_kdtree=true
run_wsqbe=false
run_kernel_vsm=false
run_lsa=false


metrics=( euclidean )
n_clusters=( 8 )
n_topics=( 500 )

echo "Starting Standford NER..."
java -mx1000m -cp $STANFORD_NER_PATH edu.stanford.nlp.ie.NERServer -loadClassifier $STANDFORD_ROOT_PATH/classifiers/english.all.3class.distsim.crf.ser.gz -port $STANFORD_NER_PORT -outputFormat inlineXML &
STANDFORD_SERVER_PID=$!
sleep $SLEEP_TIME

#mv $ROOT_PATH/experiments/babelnet/ner.log $$ROOT_PATH/experiments/babelnet/nerBackup.log


#Clustering KMeans searcher experiments
if [ "$run_kmeans" = true ] ; then
    for n in "${n_clusters[@]}"
    do
        mkdir kmeans/$n
        CLUSTERING_RAW_RESULTS_FILE=kmeans/$n/kmeans_raw_results.csv
        CLUSTERING_RESULTS_FILE=kmeans/$n/kmeans_results.txt
        sed -i "s/%s%/${n}/g" kmeans_properties.cfg
        echo -n "Starting smartweb server (KMeansSearchEngine)..."
        python $SMARTWEB_PATH -engine KMeansSearchEngine -conf kmeans_properties.cfg -port $SMARTWEB_PORT &
        SMARTWEB_SERVER_PID=$!
        sleep $SLEEP_TIME
        echo "[OK]"
        echo "Running experiments..."
        python run_experiments.py $MASHAPE_DATASET_PATH $QUERY_FILE_PATH $CLUSTERING_RAW_RESULTS_FILE --port $SMARTWEB_PORT
        python $RESULTS_PROCESSOR_PATH $HITLIST_FILE_PATH $CLUSTERING_RAW_RESULTS_FILE $CLUSTERING_RESULTS_FILE
        echo -n "Stoping smartweb server..."
        kill -9 $SMARTWEB_SERVER_PID
        sed -i "s/${n}/%s%/g" kmeans_properties.cfg
        echo "[OK]"
    done
fi

#KDTree registry experiments
if [ "$run_kdtree" = true ] ; then
    for n in "${metrics[@]}"
    do
        mkdir kdtree/$n
        KDTREE_RAW_RESULTS_FILE=kdtree/$n/kdtree_raw_results.csv
        echo "KDTREE_RAW_RESULTS_FILE: " KDTREE_RAW_RESULTS_FILE
        KDTREE_RESULTS_FILE=kdtree/$n/kdtree_results.txt
        sed -i "s/%s%/${n}/g" kdtree_properties.cfg
        echo -n "Starting smartweb server (KDTreeSearchEngine)..."
        python $SMARTWEB_PATH -engine KDTreeSearchEngine -conf kdtree_properties.cfg -port $SMARTWEB_PORT &
        SMARTWEB_SERVER_PID=$!
        sleep $SLEEP_TIME
        echo "[OK]"
        echo "Running experiments..."
        python run_experiments.py $MASHAPE_DATASET_PATH $QUERY_FILE_PATH $KDTREE_RAW_RESULTS_FILE --port $SMARTWEB_PORT
        python $RESULTS_PROCESSOR_PATH $HITLIST_FILE_PATH $KDTREE_RAW_RESULTS_FILE $KDTREE_RESULTS_FILE
        echo -n "Stoping smartweb server..."
        kill -9 $SMARTWEB_SERVER_PID
        sed -i "s/${n}/%s%/g" kdtree_properties.cfg
        echo "[OK]"
    done
fi

#WSQBE experiments
if [ "$run_wsqbe" = true ] ; then
    WSQBE_RAW_RESULTS_FILE=wsqbe/wsqbe_raw_results.csv
    WSQBE_RESULTS_FILE=wsqbe/wsqbe_results.txt
    echo -n "Starting smartweb server (WSQBESearchEngine)..."
    python $SMARTWEB_PATH -engine WSQBESearchEngine -conf wsqbe_properties.cfg -port $SMARTWEB_PORT &
    SMARTWEB_SERVER_PID=$!
    sleep $SLEEP_TIME
    echo "[OK]"
    echo "Running experiments..."
    python run_experiments.py $MASHAPE_DATASET_PATH $QUERY_FILE_PATH $WSQBE_RAW_RESULTS_FILE --port $SMARTWEB_PORT
    python $RESULTS_PROCESSOR_PATH $HITLIST_FILE_PATH $WSQBE_RAW_RESULTS_FILE $WSQBE_RESULTS_FILE
    echo -n "Stoping smartweb server..."
    kill -9 $SMARTWEB_SERVER_PID
    echo "[OK]"
fi

#Kernel VSM experiments
if [ "$run_kernel_vsm" = true ] ; then
    KERNEL_VSM_RAW_RESULTS_FILE=kernel_vsm/kernel_vsm_raw_results.csv
    KERNEL_VSM_RESULTS_FILE=kernel_vsm/kernel_vsm_results.txt
    echo -n "Starting smartweb server (KernelVSMSearchEngine)..."
    python $SMARTWEB_PATH -engine KernelVSMSearchEngine -conf kernel_vsm_properties.cfg -port $SMARTWEB_PORT &
    SMARTWEB_SERVER_PID=$!
    sleep $SLEEP_TIME
    echo "[OK]"
    echo "Running experiments..."
    python run_experiments.py $MASHAPE_DATASET_PATH $QUERY_FILE_PATH $KERNEL_VSM_RAW_RESULTS_FILE --port $SMARTWEB_PORT
    python $RESULTS_PROCESSOR_PATH $HITLIST_FILE_PATH $KERNEL_VSM_RAW_RESULTS_FILE $KERNEL_VSM_RESULTS_FILE
    echo -n "Stoping smartweb server..."
    kill -9 $SMARTWEB_SERVER_PID
    echo "[OK]"
fi

#LSA experiments
if [ "$run_lsa" = true ] ; then
    for n in "${n_topics[@]}"
    do
        mkdir lsa/$n
        LSA_RAW_RESULTS_FILE=lsa/$n/lsa_raw_results.csv
        LSA_RESULTS_FILE=lsa/$n/lsa_results.txt
        sed -i "s/%s%/${n}/g" lsa_properties.cfg
        echo -n "Starting smartweb server (LSASearchEngine)..."
        python $SMARTWEB_PATH -engine SemanticSearchEngine -conf lsa_properties.cfg -port $SMARTWEB_PORT &
        SMARTWEB_SERVER_PID=$!
        sleep $SLEEP_TIME
        echo "[OK]"
        echo "Running experiments..."
        python run_experiments.py $MASHAPE_DATASET_PATH $QUERY_FILE_PATH $LSA_RAW_RESULTS_FILE --port $SMARTWEB_PORT
        python $RESULTS_PROCESSOR_PATH $HITLIST_FILE_PATH $LSA_RAW_RESULTS_FILE $LSA_RESULTS_FILE
        echo -n "Stoping smartweb server..."
        kill -9 $SMARTWEB_SERVER_PID
        sed -i "s/${n}/%s%/g" lsa_properties.cfg
        echo "[OK]"
    done
fi

echo -n "Stoping Standford NER..."
#echo -n "Stoping SpaCy NER..."
kill -9 $STANDFORD_SERVER_PID
echo "[OK]"
