RED     := \033[1;31m
GREEN   := \033[1;32m
YELLOW  := \033[1;33m
BLUE    := \033[1;34m
PURPLE  := \033[1;35m
CYAN    := \033[1;36m
WHITE   := \033[1;37m
RESTORE := \033[0m

define message
printf "${BLUE}%s${RESTORE}\n" $(strip $1)
endef

define success
(printf "${GREEN}%s${RESTORE}\n" $(strip $1); exit 0)
endef

define warn
(printf "${YELLOW}%s${RESTORE}\n" $(strip $1); exit 0)
endef

define failure
(printf "${RED}%s${RESTORE}\n" $(strip $1); exit 1)
endef

# --- CUSTOM COMMANDS --- #

BUILD-API-IMAGE := docker compose build inference-tester
RUN-CONTAINERS := docker compose --profile test run --rm inference-tester -v
STOP-CONTAINERS := docker compose stop

# --- CUSTOM COMMANDS --- #


# --- UNIT TESTS --- #

adapter-unit-tests:
	$(call warn,"running unit tests for adapters")
	$(BUILD-API-IMAGE)
	$(RUN-CONTAINERS) tests/unit_tests/adapters -v || $(call failure,"failed in unit tests for adapters!")
	$(call success,"passed in unit tests for adapters!")

port-unit-tests:
	$(call warn,"running unit tests for ports")
	$(BUILD-API-IMAGE)
	$(RUN-CONTAINERS) tests/unit_tests/ports || $(call failure,"failed in unit tests for ports!")
	$(call success,"passed in unit tests for ports!")
	
# service-unit-tests:
# 	$(call warn,"running unit tests for services")
# 	$(BUILD-API-IMAGE)
# 	$(RUN-CONTAINERS) tests/unit_tests/services || $(call failure,"failed in unit tests for services!")
# 	$(call success,"passed in unit tests for services!")
	

all-unit-tests:
	$(MAKE) adapter-unit-tests
	$(MAKE) port-unit-tests	

# --- UNIT TESTS --- #


# --- INTEGRATION TESTS --- #

message-service-integration-tests:
	$(call warn,"running integration tests for message service")

	$(RUN-CONTAINERS) tests/integration_tests/adapters/message_service \
	    || $(call failure,"failed in integration tests for message service!")
	$(call success,"passed in integration tests for message service!")

simple-storage-integration-tests:
	$(call warn,"running integration tests for simple storage")
	$(RUN-CONTAINERS) tests/integration_tests/adapters/simple_storage \
	    || $(call failure,"failed in integration tests for simple storage!")
	$(call success,"passed in integration tests for simple storage!")
	

all-integration-tests:
	$(MAKE) message-service-integration-tests
	$(MAKE) simple-storage-integration-tests

# --- INTEGRATION TESTS --- #


# --- RUN ALL TESTS --- #
all-tests:
	$(STOP-CONTAINERS)
	$(MAKE) all-unit-tests
	$(MAKE) all-integration-tests
	$(STOP-CONTAINERS)

	