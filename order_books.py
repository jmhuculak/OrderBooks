'''
Parse order books data

Mike Widner <mikewidner@stanford.edu>
'''

import os
import csv
import sys
import argparse
import pandas as pd 


def parse_options():
    parser = argparse.ArgumentParser(
        description='Chunk files into different sizes')
    parser.add_argument('-i', dest='input', required=True,
                        help='Input file of data CSV')
    parser.add_argument('-o', dest='output', required=True,
                        help='Output path for results')
    parser.add_argument('-v', '--verbose', dest='verbose',
                        action='store_true', help='Verbose output')
    return parser.parse_args()


def check_output_path(path):
	if not os.path.exists(path):
		try:
			os.makedirs(path)
		except OSError as err:
			print(err)


def fill_empties(df):
	''' Fill empty columns with appropriate values '''
	df['Author'].fillna(method='ffill', inplace=True)	# Fill down empty authors

	# Numeric values
	columns = ['Copies Ordered', 'Pounds', 'Shillings', 'Pence']
	for col in columns:
		df[col].fillna(0, inplace=True)

	# Strings
	columns = ['Markings', 'Hand', 'Comments', 'Code / Notes']
	for col in columns:
		df[col].fillna("", inplace=True)

def convert_dates(df):
	''' Convert columns with date into date types '''
	columns = ['Date Order Received', 'Date Order Fulfilled', 'Date Payment Received']
	for col in columns:
		df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
	return df


def find_crossrefs(df):
	''' 
	Traverse the cross-references given to figure out empty dates 
	'''


def subtract_returned_copies(df):
	'''
	Find purchasers with numbers in them and "retd" or ""
	make the copies ordered a negative number
	sums should work correctly then
	'''
	pass


def write_work_puchaser_edges(df, outpath):
	# TODO: Add header source, target, weight
	df[['Title', 'Purchaser', 'Copies Ordered']].groupby(['Title', 'Purchaser']).sum().to_csv(outpath)


def sum_pounds_shillings_pence(df):
	pass


def write_hand_date_ranges(df, outpath):
	'''
	Calculate and write min-max date ranges each hand is active
	'''
	pass


def main():
	options = parse_options()
	check_output_path(options.output)
	df = pd.read_csv(options.input, quoting=0, parse_dates=['Date Order Received', 'Date Order Fulfilled', 'Date Payment Received'], dayfirst=True)
	fill_empties(df)
	df = convert_dates(df)
	df['Copies Ordered'].apply(pd.to_numeric, errors='raise')
	df_orders_by_year = df.groupby(df['Date Order Received'].dt.year)
	for year, group in df_orders_by_year:
		filename = 'work_purchaser_edges_' + str(int(year)) + '.csv'
		write_work_puchaser_edges(group, os.path.join(options.output, filename))


if __name__ == '__main__':
    if sys.version_info < (3, 0):
        print("This script requires Python 3")
        exit(-1)
    main()