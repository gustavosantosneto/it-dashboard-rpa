from dotenv import dotenv_values
import pandas as pd
import logger
import os

logger = logger.logger

ENV = dotenv_values(".env")
OUTPUT_PATH = ENV["OUTPUT_PATH"]


def convert_list_to_xlsx(filename, sheets):
    try:
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH)

        writer = pd.ExcelWriter(OUTPUT_PATH+filename, engine='xlsxwriter')

        for sheet in sheets:
            data_frame = pd.DataFrame(sheet["data"][1:])
            data_frame.to_excel(
                writer,
                sheet["name"],
                index=False,
                header=sheet["data"][0]
            )

        writer.save()
        writer.close()

        return True
    except BaseException:
        logger.exception("Falha ao gerar arquivo " + filename)
        return False
