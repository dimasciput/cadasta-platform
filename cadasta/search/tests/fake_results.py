def get_test_results(su, party, tenure_rel, resource):
    return {
          "took": 63,
          "timed_out": 'false',
          "_shards": {
            "total": 4,
            "successful": 4,
            "failed": 0
          },
          "hits": {
            "total": 4,
            "max_score": 'null',
            "hits": [{
              "_index": "project-slug",
              "_type": "location",
              "_id": su.id,
              "sort": [0],
              "_score": 'null',
              "_source": {
                "type": "CB",
                "name": "Long Island",
                "notes": "Nothing to see here.",
                "acquired_when": "2016-12-16",
                "quality": "text",
                "acquired_how": "LH"}
            }, {
              "_index": "project-slug",
              "_type": "party",
              "_id": party.id,
              "sort": [1],
              "_score": 'null',
              "_source": {
                "name": "Big Bird",
                "type": "IN",
                "gender": "M",
                "homeowner": "yes",
                "dob": "1951-05-05"
              }
            }, {
              "_index": "project-slug",
              "_type": "tenure_rel",
              "_id": tenure_rel.id,
              "sort": [1],
              "_score": 'null',
              "_source": {
                "party": "xqm9r3nymxv8pck52zgvz7t5",
                "spatial_unit": "zpeqs5uh39dhi8gr6ec3t3w5",
                "tenure_type": "CU",
                "notes": "PBS is the best."}
            }, {
              "_index": "project-slug",
              "_type": "resource",
              "_id": resource.id,
              "sort": [1],
              "_score": 'null',
              "_source": {
                "name": "Goat",
                "description": "Let's pretend there's a description.",
                "original_file": "baby_goat.jpeg"}
            },
            ]
          }
        }
