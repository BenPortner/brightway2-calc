# -*- coding: utf-8 -*-
from bw2calc.errors import OutsideTechnosphere, NonsquareTechnosphere, EmptyBiosphere
from bw2calc.lca import LCA
from pathlib import Path
import json
import pytest


fixture_dir = Path(__file__).resolve().parent / "fixtures"


def load_mapping(fp):
    return {tuple(x): y for x, y in json.load(open(fp))}


@pytest.mark.filterwarnings("ignore:no biosphere")
def test_empty_biosphere_lcia():
    fd = fixture_dir / "empty_biosphere"
    key = load_mapping(fd / "mapping.json")[("t", "1")]

    packages = [
        fd / "biosphere.zip",
        fd / "test_db.zip",
        fd / "method.zip",
    ]

    lca = LCA({key: 1}, data_objs=packages)
    lca.lci()
    with pytest.raises(EmptyBiosphere):
        lca.lcia()


def test_warning_empty_biosphere():
    fd = fixture_dir / "empty_biosphere"
    key = load_mapping(fd / "mapping.json")[("t", "1")]

    packages = [
        fd / "biosphere.zip",
        fd / "test_db.zip",
        fd / "method.zip",
    ]

    lca = LCA({key: 1}, data_objs=packages)
    with pytest.warns(UserWarning):
        lca.lci()


def test_example_db_basic():
    fd = fixture_dir / "example_db"
    mapping = load_mapping(fd / "mapping.json")

    packages = [
        fd / "example_db.zip",
        fd / "ipcc.zip",
    ]

    lca = LCA(
        {mapping[("Mobility example", "Driving an electric car")]: 1},
        data_objs=packages,
    )
    lca.lci()
    lca.lcia()
    assert lca.supply_array.sum()
    assert lca.technosphere_matrix.sum()
    assert lca.score


def test_lca_has():
    fd = fixture_dir / "example_db"
    mapping = load_mapping(fd / "mapping.json")

    packages = [
        fd / "example_db.zip",
        fd / "ipcc.zip",
    ]

    lca = LCA(
        {mapping[("Mobility example", "Driving an electric car")]: 1},
        data_objs=packages,
    )
    assert lca.has("technosphere")
    assert lca.has("characterization")
    assert not lca.has("foo")


# class LCACalculationTestCase(BW2DataTest):
#     def add_basic_biosphere(self):
#         biosphere = Database("biosphere")
#         biosphere.register()
#         biosphere.write(
#             {
#                 ("biosphere", "1"): {
#                     "categories": ["things"],
#                     "exchanges": [],
#                     "name": "an emission",
#                     "type": "emission",
#                     "unit": "kg",
#                 }
#             }
#         )

#     def test_basic(self):
#         test_data = {
#             ("t", "1"): {
#                 "exchanges": [
#                     {
#                         "amount": 0.5,
#                         "input": ("t", "2"),
#                         "type": "technosphere",
#                         "uncertainty type": 0,
#                     },
#                     {
#                         "amount": 1,
#                         "input": ("biosphere", "1"),
#                         "type": "biosphere",
#                         "uncertainty type": 0,
#                     },
#                 ],
#                 "type": "process",
#                 "unit": "kg",
#             },
#             ("t", "2"): {"exchanges": [], "type": "process", "unit": "kg"},
#         }
#         self.add_basic_biosphere()
#         test_db = Database("t")
#         test_db.register()
#         test_db.write(test_data)
#         lca = LCA({("t", "1"): 1})
#         lca.lci()
#         answer = np.zeros((2,))
#         answer[lca.dicts.activity[("t", "1")]] = 1
#         answer[lca.dicts.activity[("t", "2")]] = 0.5
#         self.assertTrue(np.allclose(answer, lca.supply_array))

#     def test_redo_lci_fails_if_activity_outside_technosphere(self):
#         self.add_basic_biosphere()
#         test_data = {
#             ("t", "1"): {
#                 "exchanges": [
#                     {"amount": 1, "input": ("biosphere", "1"), "type": "biosphere"}
#                 ]
#             }
#         }
#         test_db = Database("t")
#         test_db.register()
#         test_db.write(test_data)
#         more_test_data = {
#             ("z", "1"): {
#                 "exchanges": [
#                     {"amount": 1, "input": ("t", "1"), "type": "technosphere"}
#                 ]
#             }
#         }
#         more_test_db = Database("z")
#         more_test_db.register()
#         more_test_db.write(more_test_data)
#         lca = LCA({("t", "1"): 1})
#         lca.lci()
#         with self.assertRaises(OutsideTechnosphere):
#             lca.redo_lci({("z", "1"): 1})

#     def test_redo_lci_with_no_new_demand_no_error(self):
#         self.add_basic_biosphere()
#         test_data = {
#             ("t", "1"): {
#                 "exchanges": [
#                     {"amount": 1, "input": ("biosphere", "1"), "type": "biosphere"}
#                 ]
#             }
#         }
#         test_db = Database("t")
#         test_db.register()
#         test_db.write(test_data)
#         more_test_data = {
#             ("z", "1"): {
#                 "exchanges": [
#                     {"amount": 1, "input": ("t", "1"), "type": "technosphere"}
#                 ]
#             }
#         }
#         more_test_db = Database("z")
#         more_test_db.register()
#         more_test_db.write(more_test_data)
#         lca = LCA({("t", "1"): 1})
#         lca.lci()
#         lca.redo_lci()

#     def test_passing_falsey_key(self):
#         self.add_basic_biosphere()
#         with self.assertRaises(ValueError):
#             LCA({None: 1})
#         with self.assertRaises(ValueError):
#             LCA({(): 1})

#     def test_pass_object_as_demand(self):
#         self.add_basic_biosphere()

#         class Foo:
#             pass

#         obj = Foo()
#         with self.assertRaises(ValueError):
#             LCA(obj)

#     def test_production_values(self):
#         test_data = {
#             ("t", "1"): {
#                 "exchanges": [
#                     {
#                         "amount": 2,
#                         "input": ("t", "1"),
#                         "type": "production",
#                         "uncertainty type": 0,
#                     },
#                     {
#                         "amount": 0.5,
#                         "input": ("t", "2"),
#                         "type": "technosphere",
#                         "uncertainty type": 0,
#                     },
#                     {
#                         "amount": 1,
#                         "input": ("biosphere", "1"),
#                         "type": "biosphere",
#                         "uncertainty type": 0,
#                     },
#                 ],
#                 "type": "process",
#                 "unit": "kg",
#             },
#             ("t", "2"): {"exchanges": [], "type": "process", "unit": "kg"},
#         }
#         self.add_basic_biosphere()
#         test_db = Database("t")
#         test_db.register()
#         test_db.write(test_data)
#         lca = LCA({("t", "1"): 1})
#         lca.lci()
#         answer = np.zeros((2,))
#         answer[lca.dicts.activity[("t", "1")]] = 0.5
#         answer[lca.dicts.activity[("t", "2")]] = 0.25
#         self.assertTrue(np.allclose(answer, lca.supply_array))

#     def test_substitution(self):
#         # bw2data version 1.0 compatibility
#         if "substitution" not in TYPE_DICTIONARY:
#             return
#         test_data = {
#             ("t", "1"): {
#                 "exchanges": [
#                     {
#                         "amount": 1,
#                         "input": ("t", "2"),
#                         "type": "substitution",
#                         "uncertainty type": 0,
#                     },
#                     {
#                         "amount": 1,
#                         "input": ("biosphere", "1"),
#                         "type": "biosphere",
#                         "uncertainty type": 0,
#                     },
#                 ],
#                 "type": "process",
#                 "unit": "kg",
#             },
#             ("t", "2"): {"exchanges": [], "type": "process", "unit": "kg"},
#         }
#         self.add_basic_biosphere()
#         test_db = Database("t")
#         test_db.register()
#         test_db.write(test_data)
#         lca = LCA({("t", "1"): 1})
#         lca.lci()
#         answer = np.zeros((2,))
#         answer[lca.dicts.activity[("t", "1")]] = 1
#         answer[lca.dicts.activity[("t", "2")]] = -1
#         self.assertTrue(np.allclose(answer, lca.supply_array))

#     def test_substitution_no_type(self):
#         test_data = {
#             ("t", "1"): {
#                 "exchanges": [
#                     {
#                         "amount": -1,  # substitution
#                         "input": ("t", "2"),
#                         "type": "technosphere",
#                         "uncertainty type": 0,
#                     },
#                     {
#                         "amount": 1,
#                         "input": ("biosphere", "1"),
#                         "type": "biosphere",
#                         "uncertainty type": 0,
#                     },
#                 ],
#                 "type": "process",
#                 "unit": "kg",
#             },
#             ("t", "2"): {"exchanges": [], "type": "process", "unit": "kg"},
#         }
#         self.add_basic_biosphere()
#         test_db = Database("t")
#         test_db.register()
#         test_db.write(test_data)
#         lca = LCA({("t", "1"): 1})
#         lca.lci()
#         answer = np.zeros((2,))
#         answer[lca.dicts.activity[("t", "1")]] = 1
#         answer[lca.dicts.activity[("t", "2")]] = -1
#         self.assertTrue(np.allclose(answer, lca.supply_array))

#     def test_circular_chains(self):
#         test_data = {
#             ("t", "1"): {
#                 "exchanges": [
#                     {
#                         "amount": 0.5,
#                         "input": ("t", "2"),
#                         "type": "technosphere",
#                         "uncertainty type": 0,
#                     },
#                     {
#                         "amount": 1,
#                         "input": ("biosphere", "1"),
#                         "type": "biosphere",
#                         "uncertainty type": 0,
#                     },
#                 ],
#                 "type": "process",
#                 "unit": "kg",
#             },
#             ("t", "2"): {
#                 "exchanges": [
#                     {
#                         "amount": 0.1,
#                         "input": ("t", "1"),
#                         "type": "technosphere",
#                         "uncertainty type": 0,
#                     }
#                 ],
#                 "type": "process",
#                 "unit": "kg",
#             },
#         }
#         self.add_basic_biosphere()
#         test_db = Database("t")
#         test_db.register()
#         test_db.write(test_data)
#         lca = LCA({("t", "1"): 1})
#         lca.lci()
#         answer = np.zeros((2,))
#         answer[lca.dicts.activity[("t", "1")]] = 20 / 19.0
#         answer[lca.dicts.activity[("t", "2")]] = 10 / 19.0
#         self.assertTrue(np.allclose(answer, lca.supply_array))

#     def test_only_products(self):
#         test_data = {
#             ("t", "p1"): {"type": "product"},
#             ("t", "p2"): {"type": "product"},
#             ("t", "a1"): {
#                 "exchanges": [
#                     {"amount": 1, "input": ("t", "p1"), "type": "production",},
#                     {"amount": 1, "input": ("t", "p2"), "type": "production",},
#                 ]
#             },
#             ("t", "a2"): {
#                 "exchanges": [
#                     {"amount": 1, "input": ("t", "p2"), "type": "production",}
#                 ]
#             },
#         }
#         self.add_basic_biosphere()
#         test_db = Database("t")
#         test_db.register()
#         test_db.write(test_data)
#         lca = LCA({("t", "p1"): 1})
#         lca.lci()
#         answer = np.zeros((2,))
#         answer[lca.dicts.activity[("t", "a1")]] = 1
#         answer[lca.dicts.activity[("t", "a2")]] = -1
#         self.assertTrue(np.allclose(answer, lca.supply_array))

#     def test_activity_product_dict(self):
#         test_data = {
#             ("t", "activity 1"): {"type": "process"},
#             ("t", "activity 2"): {
#                 "exchanges": [
#                     {"amount": 1, "input": ("t", "activity 2"), "type": "production",}
#                 ]
#             },
#             ("t", "activity 3"): {
#                 "exchanges": [
#                     {"amount": 1, "input": ("t", "product 4"), "type": "production",}
#                 ]
#             },
#             ("t", "product 4"): {"type": "product"},
#         }
#         self.add_basic_biosphere()
#         test_db = Database("t")
#         test_db.write(test_data)
#         lca = LCA({("t", "activity 1"): 1})
#         lca.lci()
#         self.assertEqual(
#             [("t", "activity 1"), ("t", "activity 2"), ("t", "activity 3")],
#             sorted(lca.dicts.activity),
#         )
#         self.assertEqual(
#             [("t", "activity 1"), ("t", "activity 2"), ("t", "product 4")],
#             sorted(lca.dicts.product),
#         )

#         self.assertEqual(
#             [("t", "activity 1"), ("t", "activity 2"), ("t", "activity 3")],
#             sorted(lca.dicts.activity.reversed.values()),
#         )
#         self.assertEqual(
#             [("t", "activity 1"), ("t", "activity 2"), ("t", "product 4")],
#             sorted(lca.dicts.product.reversed.values()),
#         )

#     def test_process_product_split(self):
#         test_data = {
#             ("t", "p1"): {"type": "product"},
#             ("t", "a1"): {
#                 "exchanges": [
#                     {"amount": 1, "input": ("t", "p1"), "type": "production",},
#                     {"amount": 1, "input": ("t", "a1"), "type": "production",},
#                 ]
#             },
#             ("t", "a2"): {
#                 "exchanges": [
#                     {"amount": 1, "input": ("t", "p1"), "type": "production",}
#                 ]
#             },
#         }
#         self.add_basic_biosphere()
#         test_db = Database("t")
#         test_db.write(test_data)
#         lca = LCA({("t", "a1"): 1})
#         lca.lci()
#         answer = np.zeros((2,))
#         answer[lca.dicts.activity[("t", "a1")]] = 1
#         answer[lca.dicts.activity[("t", "a2")]] = -1
#         self.assertTrue(np.allclose(answer, lca.supply_array))

#     def test_activity_as_fu_raises_error(self):
#         test_data = {
#             ("t", "p1"): {"type": "product"},
#             ("t", "a1"): {
#                 "exchanges": [
#                     {"amount": 1, "input": ("t", "p1"), "type": "production",},
#                     {"amount": 1, "input": ("t", "a1"), "type": "production",},
#                 ]
#             },
#             ("t", "a2"): {
#                 "exchanges": [
#                     {"amount": 1, "input": ("t", "p1"), "type": "production",}
#                 ]
#             },
#         }
#         self.add_basic_biosphere()
#         test_db = Database("t")
#         test_db.write(test_data)
#         with self.assertRaises(ValueError):
#             lca = LCA({("t", "a2"): 1})
#             lca.lci()

#     def test_nonsquare_technosphere_error(self):
#         test_data = {
#             ("t", "p1"): {"type": "product"},
#             ("t", "a1"): {
#                 "exchanges": [
#                     {"amount": 1, "input": ("t", "p1"), "type": "production",},
#                     {"amount": 1, "input": ("t", "a1"), "type": "production",},
#                 ]
#             },
#         }
#         self.add_basic_biosphere()
#         test_db = Database("t")
#         test_db.write(test_data)
#         lca = LCA({("t", "a1"): 1})
#         with self.assertRaises(NonsquareTechnosphere):
#             lca.lci()

#     def test_multiple_lci_calculations(self):
#         test_data = {
#             ("t", "1"): {
#                 "exchanges": [
#                     {
#                         "amount": 1,
#                         "input": ("biosphere", "1"),
#                         "type": "biosphere",
#                         "uncertainty type": 0,
#                     }
#                 ],
#                 "type": "process",
#                 "unit": "kg",
#             },
#         }
#         self.add_basic_biosphere()
#         test_db = Database("t")
#         test_db.write(test_data)
#         lca = LCA({test_db.random(): 1})
#         lca.lci()
#         lca.lci()

#     def test_dependent_databases(self):
#         databases["one"] = {"depends": ["two", "three"]}
#         databases["two"] = {"depends": ["four", "five"]}
#         databases["three"] = {"depends": ["four"]}
#         databases["four"] = {"depends": ["six"]}
#         databases["five"] = {"depends": ["two"]}
#         databases["six"] = {"depends": []}
#         lca = LCA({("one", None): 1})
#         self.assertEqual(
#             sorted(lca.database_filepath),
#             sorted(
#                 {
#                     Database(name).filepath_processed()
#                     for name in ("one", "two", "three", "four", "five", "six")
#                 }
#             ),
#         )

#     def test_filepaths_full(self):
#         test_data = {
#             ("t", "1"): {
#                 "exchanges": [
#                     {
#                         "amount": 1,
#                         "input": ("biosphere", "1"),
#                         "type": "biosphere",
#                         "uncertainty type": 0,
#                     }
#                 ],
#                 "type": "process",
#                 "unit": "kg",
#             },
#         }
#         self.add_basic_biosphere()
#         test_db = Database("t")
#         test_db.write(test_data)
#         method = Method(("M",))
#         method.write([[("biosphere", "1"), 1.0]])
#         normalization = Normalization(("N",))
#         normalization.write([[("biosphere", "1"), 1.0]])
#         weighting = Weighting("W")
#         weighting.write([1])
#         lca = LCA({("t", "1"): 1}, method.name, weighting.name, normalization.name,)
#         self.assertEqual(
#             sorted(Database(x).filepath_processed() for x in ("biosphere", "t")),
#             sorted(lca.database_filepath),
#         )
#         self.assertEqual(lca.method_filepath, [method.filepath_processed()])
#         self.assertEqual(lca.weighting_filepath, [weighting.filepath_processed()])
#         self.assertEqual(
#             lca.normalization_filepath, [normalization.filepath_processed()]
#         )

#     def test_filepaths_empty(self):
#         test_data = {
#             ("t", "1"): {
#                 "exchanges": [
#                     {
#                         "amount": 1,
#                         "input": ("biosphere", "1"),
#                         "type": "biosphere",
#                         "uncertainty type": 0,
#                     }
#                 ],
#                 "type": "process",
#                 "unit": "kg",
#             },
#         }
#         self.add_basic_biosphere()
#         test_db = Database("t")
#         test_db.write(test_data)
#         lca = LCA({("t", "1"): 1})
#         self.assertEqual(
#             sorted(Database(x).filepath_processed() for x in ("biosphere", "t")),
#             sorted(lca.database_filepath),
#         )
#         self.assertTrue(lca.method_filepath is None)
#         self.assertTrue(lca.normalization_filepath is None)
#         self.assertTrue(lca.weighting_filepath is None)

#     def test_demand_type(self):
#         with self.assertRaises(ValueError):
#             LCA(("foo", "1"))
#         with self.assertRaises(ValueError):
#             LCA("foo")
#         with self.assertRaises(ValueError):
#             LCA([{"foo": "1"}])

#     def test_decomposed_uses_solver(self):
#         test_data = {
#             ("t", "1"): {
#                 "exchanges": [
#                     {
#                         "amount": 0.5,
#                         "input": ("t", "2"),
#                         "type": "technosphere",
#                         "uncertainty type": 0,
#                     },
#                     {
#                         "amount": 1,
#                         "input": ("biosphere", "1"),
#                         "type": "biosphere",
#                         "uncertainty type": 0,
#                     },
#                 ],
#                 "type": "process",
#                 "unit": "kg",
#             },
#             ("t", "2"): {"exchanges": [], "type": "process", "unit": "kg"},
#         }
#         self.add_basic_biosphere()
#         test_db = Database("t")
#         test_db.register()
#         test_db.write(test_data)
#         lca = LCA({("t", "1"): 1})
#         lca.lci(factorize=True)
#         # Indirect test because no easy way to test a function is called
#         lca.technosphere_matrix = None
#         self.assertEqual(float(lca.solve_linear_system().sum()), 1.5)

#     def test_fix_dictionaries(self):
#         test_data = {
#             ("t", "1"): {
#                 "exchanges": [
#                     {
#                         "amount": 0.5,
#                         "input": ("t", "2"),
#                         "type": "technosphere",
#                         "uncertainty type": 0,
#                     },
#                     {
#                         "amount": 1,
#                         "input": ("biosphere", "1"),
#                         "type": "biosphere",
#                         "uncertainty type": 0,
#                     },
#                 ],
#                 "type": "process",
#                 "unit": "kg",
#             },
#             ("t", "2"): {"exchanges": [], "type": "process", "unit": "kg"},
#         }
#         self.add_basic_biosphere()
#         test_db = Database("t")
#         test_db.register()
#         test_db.write(test_data)
#         lca = LCA({("t", "1"): 1})
#         lca.lci()

#         supply = lca.supply_array.sum()

#         self.assertTrue(lca._fixed)
#         self.assertFalse(lca.fix_dictionaries())
#         # Second time doesn't do anything
#         self.assertFalse(lca.fix_dictionaries())
#         self.assertTrue(lca._fixed)
#         lca.redo_lci({("t", "1"): 2})
#         self.assertEqual(lca.supply_array.sum(), supply * 2)

#     def test_redo_lci_switches_demand(self):
#         test_data = {
#             ("t", "1"): {
#                 "exchanges": [
#                     {
#                         "amount": 0.5,
#                         "input": ("t", "2"),
#                         "type": "technosphere",
#                         "uncertainty type": 0,
#                     },
#                     {
#                         "amount": 1,
#                         "input": ("biosphere", "1"),
#                         "type": "biosphere",
#                         "uncertainty type": 0,
#                     },
#                 ],
#                 "type": "process",
#                 "unit": "kg",
#             },
#             ("t", "2"): {"exchanges": [], "type": "process", "unit": "kg"},
#         }
#         self.add_basic_biosphere()
#         test_db = Database("t")
#         test_db.write(test_data)

#         lca = LCA({("t", "1"): 1})
#         lca.lci()
#         self.assertEqual(lca.demand, {("t", "1"): 1})

#         lca.redo_lci({("t", "1"): 2})
#         self.assertEqual(lca.demand, {("t", "1"): 2})

#     def test_basic_lcia(self):
#         test_data = {
#             ("t", "1"): {
#                 "exchanges": [
#                     {"amount": 1, "input": ("t", "2"), "type": "technosphere",}
#                 ],
#             },
#             ("t", "2"): {
#                 "exchanges": [
#                     {"amount": 1, "input": ("biosphere", "1"), "type": "biosphere",}
#                 ],
#             },
#         }
#         method_data = [(("biosphere", "1"), 42)]
#         self.add_basic_biosphere()
#         test_db = Database("t")
#         test_db.register()
#         test_db.write(test_data)

#         method = Method(("a method",))
#         method.register()
#         method.write(method_data)

#         lca = LCA({("t", "1"): 1}, ("a method",))
#         lca.lci()
#         lca.lcia()

#         self.assertTrue(np.allclose(42, lca.score))

#     def test_redo_lcia_switches_demand(self):
#         test_data = {
#             ("t", "1"): {
#                 "exchanges": [
#                     {"amount": 1, "input": ("t", "2"), "type": "technosphere",}
#                 ],
#             },
#             ("t", "2"): {
#                 "exchanges": [
#                     {"amount": 1, "input": ("biosphere", "1"), "type": "biosphere",}
#                 ],
#             },
#         }
#         method_data = [(("biosphere", "1"), 42)]
#         self.add_basic_biosphere()
#         test_db = Database("t")
#         test_db.register()
#         test_db.write(test_data)

#         method = Method(("a method",))
#         method.register()
#         method.write(method_data)

#         lca = LCA({("t", "1"): 1}, ("a method",))
#         lca.lci()
#         lca.lcia()
#         self.assertEqual(lca.demand, {("t", "1"): 1})

#         lca.redo_lcia({("t", "2"): 2})
#         self.assertEqual(lca.demand, {("t", "2"): 2})

#     def test_lcia_regionalized_ignored(self):
#         test_data = {
#             ("t", "1"): {
#                 "exchanges": [
#                     {"amount": 1, "input": ("t", "2"), "type": "technosphere",}
#                 ],
#             },
#             ("t", "2"): {
#                 "exchanges": [
#                     {"amount": 1, "input": ("biosphere", "1"), "type": "biosphere",}
#                 ],
#             },
#         }
#         method_data = [
#             (("biosphere", "1"), 21),
#             (("biosphere", "1"), 21, config.global_location),
#             (("biosphere", "1"), 100, "somewhere else"),
#         ]
#         self.add_basic_biosphere()
#         test_db = Database("t")
#         test_db.register()
#         test_db.write(test_data)

#         method = Method(("a method",))
#         method.register()
#         method.write(method_data)

#         lca = LCA({("t", "1"): 1}, ("a method",))
#         lca.lci()
#         lca.lcia()

#         self.assertTrue(np.allclose(42, lca.score))
