import psycopg2

conn = psycopg2.connect("host='ec2-54-197-253-122.compute-1.amazonaws.com' dbname='df3192mkr3k3ch' user='egtavjsibewktj' password='51fa705edf6ebe7f7e7e3f2223b9768386741a7d91bc731931820e2c7dc8f95d'")
cur = conn.cursor()