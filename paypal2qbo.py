import csv
import argparse
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='+', type=argparse.FileType('r'))
    args = parser.parse_args()

    transactions = []
    for f in args.infile:
        for line in csv.DictReader(f):
            # The single line has a gross payment and a fee payment, so we need to split those apart
            tstamp = time.strptime('{Date} { Time}'.format(**line), '%m/%d/%Y %H:%M:%S')

            # This is the "gross" payment
            transactions.append((
                tstamp,
                '{ Type} { Name}'.format(**line),
                line[' Gross']
            ))

            if line[' Fee']:
                transactions.append((
                    tstamp,
                    '{ Type} { Name} Fee'.format(**line),
                    line[' Fee']
                ))

    with open('QuickBooksOutput.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['Date', 'Description', 'Amount'])
        writer.writeheader()

        for txn in sorted(transactions, key=lambda l: l[0], reverse=True):
            writer.writerow({
                'Date': time.strftime('%m/%d/%Y %H:%M:%S', txn[0]),
                'Description': txn[1],
                'Amount': txn[2]
            })


if __name__ == '__main__':
    main()
