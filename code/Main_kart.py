import os
import datetime
import shutil

import validator as vd
import emailer as eml
from file_reader import read_files

def main_code():
    """
    Main function to process incoming order files.
    Validates each order based on multiple rules and moves the files to either success or rejected folders.
    Sends an email summary to business.
    """

    flag = False
    try:
        today_date = datetime.date.today().strftime('%d%m%y')
        email_date = datetime.date.today().strftime('%Y-%m-%d')
        subject = f'Validation email for {email_date}'
        incoming_file_path = f'../incoming_files/{today_date}'
        incoming_files = os.listdir(incoming_file_path)
        rejected_file_path = f'../rejected_files/{today_date}'
        success_file_path = f'../success_files/{today_date}'
        total_count = len(incoming_files)

        if total_count > 0:
            success_file_count = 0
            rejected_file_count = 0
            for file in incoming_files:
                products = vd.read_master_data() # Read product IDs from master
                product_info = vd.get_product_info()
                orders = read_files(f'{incoming_file_path}/{file}') # Read order lines

                if len(orders) > 0:
                    for order in orders:
                        rejected_reason = ''
                        pid_reject_reason = ''
                        empty_reject_reason = ''
                        date_reject_reason = ''
                        city_reject_reason = ''
                        sales_reject_reason = ''
                        order_dict = {}

                        data_row = order.split(',')
                        order_dict['order_id'] = data_row[0]
                        order_dict['order_date'] = data_row[1]
                        order_dict['product_id'] = data_row[2]
                        order_dict['quantity'] = data_row[3]
                        order_dict['sales'] = data_row[4]
                        order_dict['city'] = data_row[5].strip()

                        # run validations
                        valid_pro_id = vd.validate_id(order_dict['product_id'], products)
                        valid_order_date = vd.validate_order_date(order_dict['order_date'])
                        valid_city = vd.validate_city(order_dict['city'])
                        valid_empty = vd.validate_empty(order_dict)
                        valid_sales = vd.validate_sales(order_dict, product_info)

                        # collect reasons for rejection
                        if not valid_pro_id:
                            pid_reject_reason = f"Invalid product id {order_dict['product_id']}"
                            rejected_reason = rejected_reason + pid_reject_reason + ';'
                        if len(valid_empty) > 0:
                            for col in valid_empty:
                                empty_reject_reason = empty_reject_reason + col + ','
                            empty_reject_reason = 'Columns ' + empty_reject_reason.strip(',') + ' are empty.'
                            rejected_reason = rejected_reason + empty_reject_reason + ';'
                        if not valid_order_date:
                            date_reject_reason = f"Date {order_dict['order_date']} is a future date."
                            rejected_reason = rejected_reason + date_reject_reason + ';'
                        if not valid_city:
                            city_reject_reason = f"Invalid city {order_dict['city']}."
                            rejected_reason = rejected_reason + city_reject_reason + ';'
                        if not valid_sales and valid_pro_id:
                            sales_reject_reason = f'Invalid Sales calculation.'
                            rejected_reason = rejected_reason + sales_reject_reason

                        # If all validations pass, skip to next
                        if valid_pro_id and valid_sales and valid_city and valid_order_date and len(valid_empty) == 0:
                            continue
                        else:
                            row_str = ''
                            flag = False
                            if not os.path.exists(f'{rejected_file_path}'):
                                os.makedirs(f'{rejected_file_path}', exist_ok=True)
                            shutil.copy(f'{incoming_file_path}/{file}', f'{rejected_file_path}/{file}')
                            rejected_file_count += 1
                            with open(f'{rejected_file_path}/error_{file}', 'a') as fp:
                                for key in order_dict.keys():
                                    row_str = row_str + order_dict[key] + ','
                                row_str = row_str + rejected_reason
                                row_str = row_str.strip(',')
                                header = False
                                fp.write('order_id,order_date,product_id,quantity,sales,city,rejected_reason')
                                fp.write('\n')
                                header = True
                                fp.write(row_str)
                                fp.write('\n')
                                fp.close()
                    else:
                        if flag:
                            if not os.path.exists(f'{success_file_path}'):
                                os.makedirs(f'{success_file_path}', exist_ok=True)
                            shutil.copy(f'{incoming_file_path}/{file}', f'{success_file_path}/{file}')
                            success_file_count += 1

                else:
                    if not os.path.exists(f'{rejected_file_path}'):
                        os.makedirs(f'{rejected_file_path}', exist_ok=True)
                    shutil.copy(f'{incoming_file_path}/{file}', f'{rejected_file_path}/{file}')

                    with open(f'{rejected_file_path}/error_{file}', 'a') as f:
                        f.write("Empty file")
                        f.close()
                    rejected_file_count += 1
            else:
                summary = {
                    "date" : email_date,
                    "total_files" : total_count,
                    "successful_files" : success_file_count,
                    "rejected_files" : rejected_file_count
                }
                body = summary
                eml.sendmail(subject, body)
        else:
            eml.sendmail(subject, "No file present in source folder.")

    except Exception as e:
        print(str(e))

main_code()