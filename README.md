# Backend Task - Clean Architecture

This project is a very naive implementation of a simple shop system. It mimics in its structure a real world example of a service that was prepared for being split into microservices and uses the current Helu backend tech stack.

## Questions and Answers

1. Why can we not easily split this project into two microservices?
	- First of all, doesn't make sense for the business logic, because User, Item and CartItem only make sense under the same context.
	- While we've separated concerns into layers, we haven't fully established bounded contexts with clear boundaries between the `user` and `item` domains. The `add_item_to_cart` operation still crosses these boundaries.
	- Operations like adding items to a cart require data consistency across both user and item data. In a microservices world, we'd need to implement distributed transactions or eventual consistency patterns.
	- Due to this logic and business requirements, both domains share the same database. In a true microservices architecture, each service would have its own data store.	

2. Why does this project not adhere to the clean architecture even though we have seperate modules for api, repositories, usecases and the model?
	 - In clean architecture, dependencies should point inward (domain ← use cases ← adapters ← infrastructure), but here the domain models (User, Item) depend on SQLAlchemy's `Base`, violating the dependency rule.
	- The domain models are primarily data structures tied to the database rather than rich domain objects with behavior.
	- Repository implementations are directly tied to SQLAlchemy, and the domain models are defined as SQLAlchemy models rather than pure domain entities.
	- Clean architecture typically uses interfaces to define repository contracts, but this project directly uses concrete implementations.
	- Direct imports between modules violate the principle that modules should depend only on abstractions.
	
3. What would be your plan to refactor the project to stick to the clean architecture?
	- Define pure domain entities without ORM dependencies
	- Add domain services and business rules
	- Define abstract interfaces in the domain layer
	- Move implementation details to an infrastructure layer
	- Create ORM models in the infrastructure layer
	- Use dependency inversion for repositories
	- Define input/output DTOs for use cases

4. How can you make dependencies between modules more explicit?
	- Create interfaces for services needed by other modules
	- Use domain events for cross-module notifications
	- Implement event handlers for reacting to changes
	- Use configuration to specify which implementations to use
	- Separate the "what" from the "how" in module interactions

## How to use this project

If you have not installed poetry you find instructions [here](https://python-poetry.org/).

1. `docker-compose up` - runs a postgres instance for development
2. `poetry install` - install all dependency for the project
3. `poetry run schema` - creates the database schema in the postgres instance
4. `poetry run start` - runs the development server at port 8000
5. `/postman` - contains an postman environment and collections to test the project

## Other commands

* `poetry run graph` - draws a dependency graph for the project
* `poetry run tests` - runs the test suite
* `poetry run lint` - runs flake8 with a few plugins
* `poetry run format` - uses isort and black for autoformating
* `poetry run typing` - uses mypy to typecheck the project

## Specification - A simple shop

* As a customer, I want to be able to create an account so that I can save my personal information.
* As a customer, I want to be able to view detailed product information, such as price, quantity available, and product description, so that I can make an informed purchase decision.
* As a customer, I want to be able to add products to my cart so that I can easily keep track of my intended purchases.
* As an inventory manager, I want to be able to add new products to the system so that they are available for customers to purchase.