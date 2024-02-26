import csv
import json
import os
import xml.etree.ElementTree as ET
from argparse import FileType

from django.core.management.base import BaseCommand

from app.models import Poi, Category


class Command(BaseCommand):

    def __init__(self):
        self.category_cache = {
            category.name: category
            for category in Category.objects.all()
        }

    def add_arguments(self, parser):
        """
        Add custom command-line arguments to the management command.

        Args:
            parser: The argument parser object.
        """
        parser.add_argument(
            "filepath", type=FileType("r"), help="Path to the file"
        )

    def handle(self, *args, **kwargs):
        """
        Execute the command logic when the management command is run.

        Args:
            *args: Variable positional arguments.
            **kwargs: Variable keyword arguments.
        """
        try:
            filepath = kwargs["filepath"]
            extension = os.path.splitext(filepath.name)[1]

            print(f"Filepath: {filepath.name}")

            match extension:
                case ".xml":
                    print("Processing XML file")
                    self.process_xml_file(filepath)
                case ".json":
                    print("Processing JSON file")
                    self.process_json_file(filepath)
                case ".csv":
                    print("Processing CSV file")
                    self.process_csv_file(filepath)
                case _:
                    print("Filetype not supported")
        except Exception as e:
            print(f"An error occurred: {e}")
            return

    def process_xml_file(self, filepath):
        """
        Process a XML file and save the data to the database.

        Args:
            filepath (str): The path to the XML file.

        Returns:
            list: A processed list of data from the XML file.
        """
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()

            for element in root.findall("DATA_RECORD"):
                data_from_xml = self.extract_data(element, "xml")
                self.create_or_update_database_record(data_from_xml)
        except Exception as e:
            print(f"Error processing XML file: {e}")
            raise

    def process_json_file(self, filepath):
        """
        Process a JSON file and save the data to the database.

        Args:
            filepath (str): The path to the JSON file.

        Returns:
            list: A processed list of data from the JSON file.
        """

        try:
            with filepath as json_file:
                data_list = json.load(json_file)

                for item_data in data_list:
                    data_from_json = self.extract_data(
                        item_data, "json"
                    )
                    self.create_or_update_database_record(
                        data_from_json
                    )
        except Exception as e:
            print(f"Error processing JSON file: {e}")
            raise

    def process_csv_file(self, filepath):
        """
        Process a CSV file and save the data to the database.

        Args:
            filepath (str): The path to the CSV file.

        Returns:
            list: A processed list of data from the CSV file.
        """
        try:
            with filepath as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for chunk in iter(lambda: list(csv_reader), []):
                    records_to_insert = []
                    for row in chunk:
                        data_from_csv = self.extract_data(row, "csv")
                        record = Poi(**data_from_csv)
                        records_to_insert.append(record)
                    self.create_or_update_database_record(
                        records_to_insert, is_csv=True
                    )
        except Exception as e:
            print(f"Error processing CSV file: {e}")
            raise

    def extract_data(self, element, filetype):
        """
        Extract data from an element based on the provided filetype.

        Args:
            element: The data element to extract information from.
            filetype (str): The type of file associated with the data.

        Returns:
            data (dict): Extracted data from the element.
        """
        try:
            if filetype == "xml":
                avg_rating = self.get_average_rating(
                    element.find("pratings", None), "xml"
                )

                data = {
                    "name": element.find("pname").text,
                    "external_id": element.find("pid").text,
                    "category": element.find("pcategory").text,
                    "avg_rating": avg_rating,
                }
            elif filetype == "json":
                avg_rating = self.get_average_rating(
                    element.get("ratings", []), "json"
                )
                data = {
                    "name": element.get("name"),
                    "external_id": element.get("id"),
                    "category": element.get("category"),
                    "avg_rating": avg_rating,
                }
            elif filetype == "csv":
                avg_rating = self.get_average_rating(
                    element.get("poi_ratings", None), "csv"
                )
                data = {
                    "name": element.get("poi_name"),
                    "external_id": element.get("poi_id"),
                    "category": element.get("poi_category"),
                    "avg_rating": avg_rating,
                }

            if data["category"] not in self.category_cache:
                category, _ = Category.objects.get_or_create(
                    name=data["category"]
                )
                self.category_cache[data["category"]] = category

            data["category"] = self.category_cache[data["category"]]
            return data
        except Exception as e:
            print(f"Error extracting file data: {e}")
            raise

    def get_average_rating(self, ratings, filetype):
        """
        Calculate the average rating from a list of ratings.

        Args:
            ratings (list): A list of numerical ratings.
            filetype (str): The type of file.

        Returns:
            float: The average rating.

        Raises:
            Exception: If there is an issue with the average rating
                        calculation.
        """

        try:
            if ratings is not None:
                if filetype == "xml":
                    ratings_values = [
                        int(value)
                        for value in ratings.text.split(",")
                    ]
                elif filetype == "json":
                    ratings_values = [int(value) for value in ratings]
                elif filetype == "csv":
                    ratings_values = [
                        float(value)
                        for value in ratings.replace("{", "")
                        .replace("}", "")
                        .split(",")
                        if value
                    ]
                else:
                    ratings_values = []
                average_rating = (
                    sum(ratings_values) / len(ratings_values)
                    if len(ratings_values) > 0
                    else 0.0
                )
                return average_rating
            return 0
        except Exception as e:
            print(f"Error while calculating average rating: {e}")
            raise

    def create_or_update_database_record(self, data, is_csv=False):
        """
        Creates a new database record if it does not exist or updates an
                existing record.

        Args:
            data (dict): Data to be saved to the database.
            csv_check (bool): Check if the data is from a CSV file.

        Returns:


        Raises:
            Exception: If there is an issue with the database operation.
        """

        try:
            if is_csv:
                Poi.objects.bulk_create(data)
            else:
                Poi.objects.update_or_create(
                    external_id=data.get("external_id"),
                    defaults=data,
                )
        except Exception as e:
            print(f"Error while creating record in database: {e}")
            raise
