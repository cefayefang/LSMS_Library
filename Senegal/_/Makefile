rounds := $(shell ls -d ../[12]*)

source = $(shell find $(rounds) -name \*.py)
parquet := $(source:.py=.parquet)

var = ../var/food_expenditures.parquet ../var/food_quantities.parquet ../var/food_prices.parquet \
	  ../var/household_characteristics.parquet ../var/other_features.parquet 
      
all: $(parquet) $(var)

../var/food_quantities.parquet ../var/food_expenditures.parquet ../var/food_prices.parquet &: ../var/food_acquired.parquet food_acquired.py
	python food_prices_quantities_and_expenditures.py

food_acquired = $(shell find $(rounds) -name food_acquired.py)
food_acquired_parquet := $(food_acquired:.py=.parquet)

../%/_/food_acquired.parquet: $(food_acquired) ../var/other_features.parquet
	(cd $(@D) && python food_acquired.py)

../var/food_acquired.parquet: food_acquired.py $(food_acquired_parquet)
	python food_acquired.py

household_characteristics = $(shell find $(rounds) -name household_characteristics.py)
household_characteristics_parquet := $(household_characteristics:.py=.parquet)

../%/_/household_characteristics.parquet: household_characteristics.py
	(cd $(@D) && python household_characteristics.py)

../var/household_characteristics.parquet: household_characteristics.py $(household_characteristics_parquet) ../var/other_features.parquet
	python household_characteristics.py

other_features = $(shell find $(rounds) -name other_features.py)
other_features_parquet := $(other_features:.py=.parquet)

../%/_/other_features.parquet: other_features.py
	(cd $(@D) && python other_features.py)

../var/other_features.parquet: other_features.py $(other_features_parquet)
	python other_features.py

%.parquet: %.py food_items.org senegal.py
	(cd $(@D) && python ./$(<F))

clean:
	-rm $(parquet)
	-rm ../var/*.parquet
