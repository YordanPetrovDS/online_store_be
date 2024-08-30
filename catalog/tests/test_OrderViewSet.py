from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from catalog.models import Order, OrderProduct, Product  # noqa: F401

UserModel = get_user_model()


class OrderViewSetTests(APITestCase):
    VALID_USER_DATA = {
        "username": "Doncho",
        "email": "doncho@abv.bg",
        "password": "Newlife7",
    }

    def _create_user_and_login(self, user_data: dict, is_staff=False):
        if is_staff:
            user = UserModel.objects.create_superuser(**user_data)
        else:
            user = UserModel.objects.create_user(**user_data)

        login_data = {key: item for key, item in user_data.items() if key != "email"}

        self.client.post(reverse("accounts:login"), login_data)

        return user

    def test_create_order__when_user_is_not_auth__should_raise(self):
        sample_data = {
            "date": "2022-11-01",
        }
        response = self.client.post(reverse("catalog:orders-list"), sample_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order__when_data_is_valid__expect_to_create(self):
        user = self._create_user_and_login(self.VALID_USER_DATA)

        sample_data = {
            "date": "2022-11-01",
        }

        response = self.client.post(
            reverse("catalog:orders-list"),
            sample_data,
            HTTP_AUTHORIZATION=f"token {user.auth_token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["date"], sample_data["date"])

    def test_update_order__when_user_is_not_auth__should_raise(self):
        sample_data = {
            "date": "2022-11-01",
        }
        response = self.client.put(reverse("catalog:orders-list"), sample_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_order__when_data_is_valid__expect_to_update(self):
        user = self._create_user_and_login(self.VALID_USER_DATA)

        sample_data = {
            "date": "2022-11-01",
        }
        response = self.client.post(
            reverse("catalog:orders-list"),
            sample_data,
            HTTP_AUTHORIZATION=f"token {user.auth_token.key}",
        )

        order = Order.objects.first()

        new_data = {
            "date": "2023-02-01",
        }
        response = self.client.put(
            reverse("catalog:orders-detail", kwargs={"pk": order.id}),
            new_data,
            HTTP_AUTHORIZATION=f"token {user.auth_token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["date"], new_data["date"])

    def test_delete_order__when_order_id_is_valid__expect_to_delete(self):
        user = self._create_user_and_login(self.VALID_USER_DATA)

        sample_data = {
            "date": "2022-11-01",
        }
        response = self.client.post(
            reverse("catalog:orders-list"),
            sample_data,
            HTTP_AUTHORIZATION=f"token {user.auth_token.key}",
        )

        order = Order.objects.first()

        response = self.client.delete(
            reverse("catalog:orders-detail", kwargs={"pk": order.id}),
            HTTP_AUTHORIZATION=f"token {user.auth_token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_orders__when_user_is_not_admin__expect_all_orders_of_the_user(
        self,
    ):
        user_1 = self._create_user_and_login(self.VALID_USER_DATA)

        user_2_data = {
            "username": "Petko",
            "email": "doncho1@abv.bg",
            "password": "Newlife7",
        }
        user_2 = self._create_user_and_login(user_2_data)

        orders_to_create = (
            Order(date="2023-02-01", user=user_1),
            Order(date="2023-03-01", user=user_1),
            Order(date="2023-04-01", user=user_1),
            Order(date="2023-05-01", user=user_1),
            Order(date="2023-06-01", user=user_2),
            Order(date="2023-07-01", user=user_2),
            Order(date="2023-08-01", user=user_2),
            Order(date="2023-09-01", user=user_2),
        )
        Order.objects.bulk_create(orders_to_create)

        orders = Order.objects.filter(user_id=user_1.id)

        response = self.client.get(
            reverse("catalog:orders-list"),
            HTTP_AUTHORIZATION=f"token {user_1.auth_token.key}",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), len(orders))
        for idx in range(len(orders)):
            response_order_id = response.data["results"][idx]["id"]
            response_order_date = response.data["results"][idx]["date"]
            response_order_user_id = response.data["results"].serializer.context["request"].user.id
            expected_order_id = orders[idx].id
            expected_order_date = orders[idx].date.strftime("%Y-%m-%d")
            expected_order_user_id = orders[idx].user.id

            self.assertEqual(response_order_id, expected_order_id)
            self.assertEqual(response_order_date, expected_order_date)
            self.assertEqual(response_order_user_id, expected_order_user_id)

    def test_get_orders__when_user_is_admin__expect_all_orders(self):
        user_1 = self._create_user_and_login(self.VALID_USER_DATA, True)

        user_2_data = {
            "username": "Petko",
            "email": "doncho1@abv.bg",
            "password": "Newlife7",
        }
        user_2 = self._create_user_and_login(user_2_data)

        orders_to_create = (
            Order(date="2023-02-01", user=user_1),
            Order(date="2023-03-01", user=user_1),
            Order(date="2023-04-01", user=user_1),
            Order(date="2023-05-01", user=user_1),
            Order(date="2023-06-01", user=user_2),
            Order(date="2023-07-01", user=user_2),
            Order(date="2023-08-01", user=user_2),
            Order(date="2023-09-01", user=user_2),
        )
        Order.objects.bulk_create(orders_to_create)

        orders = Order.objects.all()

        response_1 = self.client.get(
            reverse("catalog:orders-list"),
            data={"page": 1},
            HTTP_AUTHORIZATION=f"token {user_1.auth_token.key}",
        )

        response_2 = self.client.get(
            reverse("catalog:orders-list"),
            data={"page": 2},
            HTTP_AUTHORIZATION=f"token {user_1.auth_token.key}",
        )

        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_1.data["results"]), 5)
        self.assertEqual(len(response_2.data["results"]), 3)
        self.assertEqual(
            len(response_1.data["results"]) + len(response_2.data["results"]),
            len(orders),
        )

        response = response_1.data["results"] + response_2.data["results"]

        for idx in range(len(orders)):
            response_order_id = response[idx]["id"]
            response_order_date = response[idx]["date"]
            expected_order_id = orders[idx].id
            expected_order_date = orders[idx].date.strftime("%Y-%m-%d")

            self.assertEqual(response_order_id, expected_order_id)
            self.assertEqual(response_order_date, expected_order_date)

    def test_stats_orders__when_user_is_not_auth__should_raise(self):
        # Act
        response_price = self.client.get(
            reverse("catalog:orders-stats"),
            data={
                "date_start": "2023-02-01",
                "date_end": "2023-06-01",
                "metric": "price",
            },
        )

        response_count = self.client.get(
            reverse("catalog:orders-stats"),
            data={
                "date_start": "2023-02-01",
                "date_end": "2023-06-01",
                "metric": "count",
            },
        )

        # Assert
        self.assertEqual(response_price.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_count.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_stats_orders__when_user_is_admin__expect_all_orders(self):
        # Arrange
        user_1_data = {
            "username": "Petko",
            "email": "doncho1@abv.bg",
            "password": "Newlife7",
        }
        admin = self._create_user_and_login(self.VALID_USER_DATA, True)
        user_1 = self._create_user_and_login(user_1_data)

        p1 = Product(title="Mouse", price=10.00, stock=10, base_price=10.00, slug="mouse")
        p2 = Product(title="Keyboard", price=50.00, stock=10, base_price=10.00, slug="keyboard")
        p1.save()
        p2.save()

        ord_1 = Order(date="2023-02-01", user=admin)
        ord_2 = Order(date="2023-03-01", user=admin)
        ord_3 = Order(date="2023-04-01", user=admin)
        ord_4 = Order(date="2023-05-01", user=admin)
        ord_5 = Order(date="2023-06-01", user=user_1)
        ord_1.save()
        ord_2.save()
        ord_3.save()
        ord_4.save()
        ord_5.save()

        op1 = OrderProduct(order=ord_1, product=p1, quantity=1, price=p1.price)
        op2 = OrderProduct(order=ord_2, product=p1, quantity=1, price=p1.price)
        op3 = OrderProduct(order=ord_3, product=p1, quantity=1, price=p1.price)
        op4 = OrderProduct(order=ord_4, product=p1, quantity=1, price=p1.price)
        op5 = OrderProduct(order=ord_5, product=p2, quantity=2, price=p2.price)
        op1.save()
        op2.save()
        op3.save()
        op4.save()
        op5.save()

        expected_result_price = [
            {"month": "2023 February", "value": 10},
            {"month": "2023 March", "value": 10},
            {"month": "2023 April", "value": 10},
            {"month": "2023 May", "value": 10},
            {"month": "2023 June", "value": 100},
        ]

        expected_result_count = [
            {"month": "2023 February", "value": 1},
            {"month": "2023 March", "value": 1},
            {"month": "2023 April", "value": 1},
            {"month": "2023 May", "value": 1},
            {"month": "2023 June", "value": 2},
        ]

        # Act
        response_price = self.client.get(
            reverse("catalog:orders-stats"),
            data={
                "date_start": "2023-02-01",
                "date_end": "2023-06-01",
                "metric": "price",
            },
            HTTP_AUTHORIZATION=f"token {admin.auth_token.key}",
        )

        response_count = self.client.get(
            reverse("catalog:orders-stats"),
            data={
                "date_start": "2023-02-01",
                "date_end": "2023-06-01",
                "metric": "count",
            },
            HTTP_AUTHORIZATION=f"token {admin.auth_token.key}",
        )

        # Assert
        self.assertEqual(response_price.status_code, status.HTTP_200_OK)
        self.assertEqual(response_count.status_code, status.HTTP_200_OK)
        self.assertEqual(response_price.data["results"], expected_result_price)
        self.assertEqual(response_count.data["results"], expected_result_count)

    def test_stats_orders__when_user_is_not_admin__expect_all_orders_of_the_user(
        self,
    ):
        user_1_data = {
            "username": "Petko",
            "email": "doncho1@abv.bg",
            "password": "Newlife7",
        }
        admin = self._create_user_and_login(self.VALID_USER_DATA, True)
        user_1 = self._create_user_and_login(user_1_data)

        # Arrange
        p1 = Product(title="Mouse", price=10.00, stock=10, base_price=10.00, slug="mouse")
        p2 = Product(title="Keyboard", price=50.00, stock=10, base_price=10.00, slug="keyboard")
        p1.save()
        p2.save()

        ord_1 = Order(date="2023-02-01", user=admin)
        ord_2 = Order(date="2023-03-01", user=admin)
        ord_3 = Order(date="2023-04-01", user=admin)
        ord_4 = Order(date="2023-05-01", user=admin)
        ord_5 = Order(date="2023-06-01", user=user_1)
        ord_6 = Order(date="2023-07-01", user=user_1)
        ord_1.save()
        ord_2.save()
        ord_3.save()
        ord_4.save()
        ord_5.save()
        ord_6.save()

        op1 = OrderProduct(order=ord_1, product=p1, quantity=1, price=p1.price)
        op2 = OrderProduct(order=ord_2, product=p1, quantity=1, price=p1.price)
        op3 = OrderProduct(order=ord_3, product=p1, quantity=1, price=p1.price)
        op4 = OrderProduct(order=ord_4, product=p1, quantity=1, price=p1.price)
        op5 = OrderProduct(order=ord_5, product=p2, quantity=1, price=p2.price)
        op6 = OrderProduct(order=ord_6, product=p2, quantity=4, price=p2.price)
        op1.save()
        op2.save()
        op3.save()
        op4.save()
        op5.save()
        op6.save()

        expected_result_price = [
            {"month": "2023 June", "value": 50},
            {"month": "2023 July", "value": 200},
        ]

        expected_result_count = [
            {"month": "2023 June", "value": 1},
            {"month": "2023 July", "value": 4},
        ]

        # Act
        response_price = self.client.get(
            reverse("catalog:orders-stats"),
            data={
                "date_start": "2023-02-01",
                "date_end": "2023-07-01",
                "metric": "price",
            },
            HTTP_AUTHORIZATION=f"token {user_1.auth_token.key}",
        )

        response_count = self.client.get(
            reverse("catalog:orders-stats"),
            data={
                "date_start": "2023-02-01",
                "date_end": "2023-07-01",
                "metric": "count",
            },
            HTTP_AUTHORIZATION=f"token {user_1.auth_token.key}",
        )

        # Assert
        self.assertEqual(response_price.status_code, status.HTTP_200_OK)
        self.assertEqual(response_count.status_code, status.HTTP_200_OK)
        self.assertEqual(response_price.data["results"], expected_result_price)
        self.assertEqual(response_count.data["results"], expected_result_count)

    def test_stats_orders__when_missing_query_params__should_raise(self):
        user_1_data = {
            "username": "Petko",
            "email": "doncho@abv.bg",
            "password": "Newlife7",
        }
        user = self._create_user_and_login(user_1_data)

        # Act
        response = self.client.get(
            reverse("catalog:orders-stats"),
            data={
                "date_end": "2023-07-01",
                "metric": "count",
            },
            HTTP_AUTHORIZATION=f"token {user.auth_token.key}",
        )

        # Assert
        self.assertEqual(response.exception, True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0]["message"], "There is missing filter field 'date_start'")

        # Act
        response = self.client.get(
            reverse("catalog:orders-stats"),
            data={
                "date_start": "2023-02-01",
                "metric": "count",
            },
            HTTP_AUTHORIZATION=f"token {user.auth_token.key}",
        )

        # Assert
        self.assertEqual(response.exception, True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0]["message"], "There is missing filter field 'date_end'")

        # Act
        response = self.client.get(
            reverse("catalog:orders-stats"),
            data={
                "date_start": "2023-02-01",
                "date_end": "2023-07-01",
            },
            HTTP_AUTHORIZATION=f"token {user.auth_token.key}",
        )

        # Assert
        self.assertEqual(response.exception, True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0]["message"], "There is missing filter field 'metric'")

        # Act
        response = self.client.get(
            reverse("catalog:orders-stats"),
            HTTP_AUTHORIZATION=f"token {user.auth_token.key}",
        )

        # Assert
        self.assertEqual(response.exception, True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_stats_orders__when_invalid_query_params__should_raise(self):
        user_1_data = {
            "username": "Petko",
            "email": "doncho@abv.bg",
            "password": "Newlife7",
        }
        user = self._create_user_and_login(user_1_data)

        # Act
        response = self.client.get(
            reverse("catalog:orders-stats"),
            data={
                "date_start": 234,
                "date_end": "2023-07-01",
                "metric": "count",
            },
            HTTP_AUTHORIZATION=f"token {user.auth_token.key}",
        )

        # Assert
        self.assertEqual(response.exception, True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data[0]["message"], "Incorrect data format for param 'date_start', should be YYYY-MM-DD"
        )

        # Act
        response = self.client.get(
            reverse("catalog:orders-stats"),
            data={
                "date_start": "2023-02-01",
                "date_end": 234,
                "metric": "count",
            },
            HTTP_AUTHORIZATION=f"token {user.auth_token.key}",
        )

        # Assert
        self.assertEqual(response.exception, True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data[0]["message"], "Incorrect data format for param 'date_end', should be YYYY-MM-DD"
        )

        # Act
        response = self.client.get(
            reverse("catalog:orders-stats"),
            data={
                "date_start": "2023-02-01",
                "date_end": "2023-07-01",
                "metric": 123,
            },
            HTTP_AUTHORIZATION=f"token {user.auth_token.key}",
        )

        # Assert
        self.assertEqual(response.exception, True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data[0]["message"], "Incorrect value for filter field 'metric', correct values are: price, count"
        )

    def test_stats_orders__when_empty_query_params__should_raise(self):
        user_1_data = {
            "username": "Petko",
            "email": "doncho@abv.bg",
            "password": "Newlife7",
        }
        user = self._create_user_and_login(user_1_data)

        # Act
        response = self.client.get(
            reverse("catalog:orders-stats"),
            data={
                "date_start": "",
                "date_end": "2023-07-01",
                "metric": "count",
            },
            HTTP_AUTHORIZATION=f"token {user.auth_token.key}",
        )

        # Assert
        self.assertEqual(response.exception, True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0]["message"], "date_start is empty")

        # Act
        response = self.client.get(
            reverse("catalog:orders-stats"),
            data={
                "date_start": "2023-02-01",
                "date_end": "",
                "metric": "count",
            },
            HTTP_AUTHORIZATION=f"token {user.auth_token.key}",
        )

        # Assert
        self.assertEqual(response.exception, True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0]["message"], "date_end is empty")

        # Act
        response = self.client.get(
            reverse("catalog:orders-stats"),
            data={
                "date_start": "2023-02-01",
                "date_end": "2023-07-01",
                "metric": "",
            },
            HTTP_AUTHORIZATION=f"token {user.auth_token.key}",
        )

        # Assert
        self.assertEqual(response.exception, True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0]["message"], "metric is empty")

    def test_stats_orders__when_query_params_are_more_that_the_required_3__should_raise(
        self,
    ):
        user_1_data = {
            "username": "Petko",
            "email": "doncho@abv.bg",
            "password": "Newlife7",
        }
        user = self._create_user_and_login(user_1_data)

        # Act
        response = self.client.get(
            reverse("catalog:orders-stats"),
            data={
                "date_start": "2023-02-01",
                "date_end": "2023-07-01",
                "metric": "count",
                "date": "2023-02-01",
            },
            HTTP_AUTHORIZATION=f"token {user.auth_token.key}",
        )

        # Assert
        self.assertEqual(response.exception, True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data[0]["message"],
            "The query params should be only the following ones - date_start,date_end,metric",
        )
