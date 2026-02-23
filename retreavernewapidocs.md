# Retreaver Core 0.1 API Reference

## Table of Contents

- [Introduction](#introduction)
  - [Version](#version)
  - [Multi-format](#multi-format)
  - [Nomenclature](#nomenclature)
  - [Our IDs vs Customer IDs](#our-ids-vs-customer-ids)
  - [Paginated](#paginated)
  - [Trees](#trees)
- [Authentication](#authentication)
- [Calls](#calls)
  - [V1 - Get recent Calls](#v1---get-recent-calls)
  - [V1 - Enumerate through all calls](#v1---enumerate-through-all-calls)
  - [V1 - Enumerate through Calls in a specific date/time range](#v1---enumerate-through-calls-in-a-specific-datetime-range)
  - [V1 - Get a specific Call](#v1---get-a-specific-call)
  - [V2 - Get recent Calls](#v2---get-recent-calls)
  - [V2 - Enumerate through all calls](#v2---enumerate-through-all-calls)
  - [V2 - Enumerate through Calls in a specific date/time range](#v2---enumerate-through-calls-in-a-specific-datetime-range)
  - [V2 - Get a specific Call](#v2---get-a-specific-call)
  - [V3 - Calls](#v3---calls)
  - [Call Data Writing](#call-data-writing)
- [Affiliates](#affiliates)
  - [Get all Affiliates](#get-all-affiliates)
  - [Get a specific Affiliate by your ID](#get-a-specific-affiliate-by-your-id)
  - [Create an Affiliate](#create-an-affiliate)
  - [Update an Affiliate](#update-an-affiliate)
  - [Remove an affiliate](#remove-an-affiliate)
- [Targets](#targets)
  - [Get all Targets](#get-all-targets)
  - [Get a specific Target](#get-a-specific-target)
  - [Create a Target](#create-a-target)
  - [Update a Target](#update-a-target)
  - [Remove a Target](#remove-a-target)
  - [Tagging a Target](#tagging-a-target)
  - [Changing a Target's Caps](#changing-a-targets-caps)
  - [Resetting a Hard Cap](#resetting-a-hard-cap)
- [Campaigns](#campaigns)
  - [Get all Campaigns](#get-all-campaigns)
  - [Get a specific Campaign](#get-a-specific-campaign)
  - [Create a Campaign](#create-a-campaign)
  - [Update a Campaign](#update-a-campaign)
  - [Remove a Campaign](#remove-a-campaign)
- [Numbers](#numbers)
  - [Get all Numbers](#get-all-numbers)
  - [Get a specific Number](#get-a-specific-number)
  - [Create a Number](#create-a-number)
  - [Update a Number](#update-a-number)
  - [Remove a Number](#remove-a-number)
- [Number Pools](#number-pools)
  - [Get all Number Pools](#get-all-number-pools)
  - [Get a specific Number Pool](#get-a-specific-number-pool)
  - [Create a Number Pool](#create-a-number-pool)
  - [Update a Number Pool](#update-a-number-pool)
  - [Remove a Number Pool](#remove-a-number-pool)
- [Companies](#companies)
  - [Get the active Company](#get-the-active-company)
  - [Get a specific Company](#get-a-specific-company)
  - [Get all Companies](#get-all-companies)
  - [Create a Company](#create-a-company)
  - [Update a Company](#update-a-company)
  - [Remove a Company](#remove-a-company)

---

## Introduction

The Retreaver Core API can be used to automate core business processes, like changing where calls are routed, and many other features that would normally be accessed through our account portal.

If you're looking for information on tracking visitors and displaying phone numbers on your landing pages, please see our [Retreaver.js](https://github.com/retreaver/retreaver-js) library.

The API can be used to automate core business processes, but does not currently support all functionality.

**Please note:** We're currently working on a better, versioned replacement for this API. But don't worry, this API isn't going away.

### Version

This is our *unversioned* API and for sake of clarity we'll refer to it henceforth as:

`Retreaver Core API`

### Multi-format

The Retreaver Core API can be accessed by JSON or XML. Simply change the file extension and Content-Type header to match your preferences.

We recommend using JSON since XML is archaic, has high overhead, and is generally awful.

| Format | Content-Type | Extension |
|--------|--------------|-----------|
| JSON | application/json | json |
| XML | text/xml | xml |

### Nomenclature

Retreaver has gone through many revisions and currently uses two new sets of terms to refer to objects. Please note, this API uses our Old nomenclature.

| Old | Performance Marketing Edition | Enterprise Edition |
|-----|------------------------------|-------------------|
| Affiliate | Publisher | Source |
| Target | Buyer | Contact Handler/Call Endpoint |
| Target Group | Buyer Group | Handler Group |

### Our IDs vs Customer IDs

For convenience, some objects can be accessed both by the IDs set by our customers and by our internal IDs.

Affiliates, Targets, and Campaigns can be accessed via customer editable IDs as "afid", "tid", and "cid" respectively.

The "id" property in the JSON/XML document refers to our internal ID.

| Object | Our Internal ID URL | Customer Editable ID URL | Customer Editable ID Accessor |
|--------|--------------------|-----------------------|------------------------------|
| Affiliate | /affiliates/{id} | /affiliates/afid/{afid} | afid |
| Target | /targets/{id} | /targets/tid/{tid} | tid |
| Campaign | /campaigns/{id} | /campaigns/cid/{cid} | cid |

These URLs work with GET, PUT, and DELETE HTTP verbs.

Please note, in many sections of the documentation below, we are referring to the Customer Editable ID URL.

### Paginated

Retreaver is a RESTful paginated API that returns 25 results per page. Each relevant index response will have a [Link HTTP header](https://www.w3.org/wiki/LinkHeader) present.

```
Link: <https://retreaver.com/calls.json?api_key=woofwoofwoof&company_id=1&sort_by=created_at&order=asc&page=6996>; rel="last", <https://retreaver.com/calls.json?api_key=woofwoofwoof&company_id=1&sort_by=created_at&order=asc&page=2>; rel="next"
```

By parsing the Link header, you can determine the last, next, and previous pages.

### Trees

Please note, for brevity, in appropriate places we have truncated the API output by eliminating properties of certain objects. We're also trying to save some trees in case someone actually tries to print this.

---

## Authentication

To authorize, use this code:

```bash
# With cURL, you can just pass the correct API key and company_id with each request.
curl "https://api.retreaver.com/call.json?api_key=woofwoofwoof&company_id=1"
```

Make sure to replace `woofwoofwoof` with your API key.

Retreaver uses API keys to allow access to the API. You can register a new Retreaver Core API key at our [account portal](https://retreaver.com/users/sign_up).

If you have a Retreaver account, you can find your Core API key at the bottom of your [user page](https://retreaver.com/users/edit).

Retreaver expects for the API key to be included in all API requests to the server in a query string parameter that looks like the following:

```
?api_key=woofwoofwoof
```

You must replace `woofwoofwoof` with your personal API key.

If you have access to more than one company on Retreaver, you must also pass in the company ID of the company you want to work with:

```
?api_key=woofwoofwoof&company_id=1
```

You can [find your company ID here](https://retreaver.com/company). We suggest passing it in anyways.

You should **never, ever expose your Retreaver Core API key publicly** as it can be used to access your entire Retreaver account without restriction!

If you suspect your API key has been publicly exposed, [reset it](https://support.retreaver.com/faq/how-do-i-get-my-api-key/).

---

## Calls

Or, more precisely, phone calls. All of the reference for V1 and V2 are applicable to V3, and V3 simply returns more fields. Just, just use the V3 /calls api.

### V1 - Get recent Calls

```bash
curl "https://api.retreaver.com/calls.json?api_key=woofwoofwoof&company_id=1"
```

The above command returns JSON structured like this:

```json
[{
   "call":{
      "uuid":"addcf985-017e-4962-be34-cf5d55e74afc",
      "caller":"+17195220377",
      "caller_zip":"80920",
      "caller_state":"CO",
      "caller_city":"COLORADO SPRINGS",
      "caller_country":"US",
      "dialed_call_duration":193,
      "total_duration":204,
      "status":"finished",
      "start_time":"2012-04-29T12:29:40Z",
      "forwarded_time":"2012-04-29T12:29:51Z",
      "end_time":"2012-04-29T12:32:46Z",
      "cid":"0003",
      "afid":"03994",
      "sid":null,
      "dialed_number":"+18668987878",
      "updated_at":"2012-04-29T12:29:46Z",
      "created_at":"2012-04-29T12:29:40Z",
      "recording_url":"http://callpixels.com/recordings/87d43a5f5c88041687f9fd1bb6a58d6f/call_17192096019_1342303189.mp3"
   }
},
{
   "call":{
      "uuid":"8ae0aa38-0173-4e62-5342-cf5d55e74afe",
      "caller":"+14166686981",
      "caller_zip":null,
      "caller_state":"ON",
      "caller_city":"TORONTO",
      "caller_country":"CA",
      "dialed_call_duration":33,
      "total_duration":40,
      "status":"finished",
      "start_time":"2012-04-29T12:29:40Z",
      "forwarded_time":"2012-04-29T12:29:51Z",
      "end_time":"2012-04-29T12:32:46Z",
      "cid":"0003",
      "afid":"03994",
      "sid":null,
      "dialed_number":"+18668987878",
      "updated_at":"2012-04-29T12:29:46Z",
      "created_at":"2012-04-29T12:29:40Z",
      "recording_url":"http://callpixels.com/recordings/87d43a5f5c88041687f9fd1bb6a58d6f/call_17192096019_1342303189.mp3"
   }
}]
```

Provides access to the call log. The call log contains all the Calls which have been made.

#### HTTP Request

`GET https://api.retreaver.com/calls.json?api_key=woofwoofwoof&company_id=1`

#### Query Parameters

| Parameter | Format | Default | Description |
|-----------|--------|---------|-------------|
| company_id | `123456` | | Return any Calls associated to the specific company IF you have access to that company. |
| created_at_start | `YYYY-MM-DDTHH:MM:SS+HH:MM` | -4712-01-01T00:00:00+00:00 | Return any Calls that were created after this date. |
| created_at_end | `YYYY-MM-DDTHH:MM:SS+HH:MM` | 4712-01-01T00:00:00+00:00 | Return any Calls that were created before this date. |
| sort_by | `created_at` or `updated_at` | `created_at` | Calls will be sorted by this value. If you only want recently updated Calls, sort by `updated_at`. Note that calls sorted by `updated_at` will forcefully be returned in `desc` order even if order parameter is `asc`. |
| order | `asc` or `desc` | `desc` | Calls will be sorted in ascending or descending order of their `sort_by` column. |
| caller | `%2B13015236555` | | Return only calls from the specified caller number. |
| client_afid | `123456` | | Return calls for an affiliate. |
| client_cid | `123456` | | Return calls for a specific campaign. |
| client_tid | `123456` | | Return calls for a specific target. |
| sub_id | `123456` | | Return calls for a affiliate Sub ID. |

### V1 - Enumerate through all calls

First page:

```bash
curl "https://api.retreaver.com/calls.json?api_key=woofwoofwoof&company_id=1&sort_by=created_at&order=asc&page=1"
```

Second page:

```bash
curl "https://api.retreaver.com/calls.json?api_key=woofwoofwoof&company_id=1&sort_by=created_at&order=asc&page=2"
```

To fetch all Calls on your Account, use the `sort_by` and `order` params to return your Calls in the order they were created, and then paginate through all your calls.

#### HTTP Request

```
https://api.retreaver.com/calls.json?api_key=woofwoofwoof&company_id=1&sort_by=created_at&order=asc&page=1
https://api.retreaver.com/calls.json?api_key=woofwoofwoof&company_id=1&sort_by=created_at&order=asc&page=2
```

### V1 - Enumerate through Calls in a specific date/time range

```bash
curl "https://api.retreaver.com/calls.json?api_key=woofwoofwoof&company_id=1&created_at_start=2016-01-01T00:00:00+00:00&created_at_end=2016-01-02T00:00:00+00:00&page=1"
```

By passing in `created_at_start` and `created_at_end` parameters, you can control the start and end time of Calls returned.

The timestamp should be formatted according to [rfc3339](https://validator.w3.org/feed/docs/error/InvalidRFC3339Date.html)

#### HTTP Request

`GET https://api.retreaver.com/calls.json?api_key=woofwoofwoof&company_id=1&created_at_start=2016-01-01T00:00:00+00:00&created_at_end=2016-01-02T00:00:00+00:00&page=1`

### V1 - Get a specific Call

Getting a specific call is possible by using the specific UUID of the call in question.

```bash
curl "https://api.retreaver.com/calls/addcf985-017e-4962-be34-cf5d55e74afc.json?api_key=woofwoofwoof&company_id=1"
```

The above command returns JSON structured like this:

```json
{
   "call":{
      "uuid":"addcf985-017e-4962-be34-cf5d55e74afc",
      "caller":"+17195220377",
      "caller_zip":"80920",
      "caller_state":"CO",
      "caller_city":"COLORADO SPRINGS",
      "caller_country":"US",
      "dialed_call_duration":193,
      "total_duration":204,
      "status":"finished",
      "start_time":"2012-04-29T12:29:40Z",
      "forwarded_time":"2012-04-29T12:29:51Z",
      "end_time":"2012-04-29T12:32:46Z",
      "cid":"0003",
      "afid":"03994",
      "sid":null,
      "dialed_number":"+18668987878",
      "updated_at":"2012-04-29T12:29:46Z",
      "created_at":"2012-04-29T12:29:40Z",
      "recording_url":"http://callpixels.com/recordings/87d43a5f5c88041687f9fd1bb6a58d6f/call_17192096019_1342303189.mp3"
   }
}
```

Calls can be accessed by their UUID.

#### HTTP Request

`GET https://api.retreaver.com/calls/addcf985-017e-4962-be34-cf5d55e74afc.json?api_key=woofwoofwoof`

### V1 - Get a calls by the caller ID, and read call_flow_options

Sometimes, you will want to filter the general calls endpoint by a specific caller ID. You can do this by adding the &caller= parameter to the request, with the value of the specific caller ID. Typically when this parameter is used, you typically will also add &call_flow_events=true, which will give you information about the calls journey in retreaver as well. Things like why calls didnt connect etc. Useful for troubleshooting. Below is an example:

#### HTTP Request

`GET https://api.retreaver.com/calls/.json?api_key=woofwoofwoof&caller=4375189332&call_flow_events=true`

the above returns:

[
  {
    "call": {
      "uuid": "f8de3d5a-0681-485f-8d04-1098b710aa09",
      "caller": "+16146792390",
      "caller_number_sent": null,
      "caller_zip": null,
      "caller_state": "OH",
      "caller_city": "COLUMBUS",
      "caller_country": "US",
      "dialed_call_duration": 0,
      "total_duration": 36,
      "ivr_duration": 36,
      "hold_duration": 0,
      "status": "finished",
      "start_time": "2026-02-21T01:04:15.814Z",
      "forwarded_time": null,
      "end_time": "2026-02-21T01:04:52.801Z",
      "cid": "1",
      "afid": null,
      "sid": null,
      "dialed_number": null,
      "revenue": null,
      "payout": null,
      "postback_value": null,
      "network_sale_timer_fired": null,
      "affiliate_sale_timer_fired": null,
      "target_sale_timer_fired": null,
      "hung_up_by": "caller",
      "duplicate": false,
      "payable_duplicate": false,
      "receivable_duplicate": false,
      "callpixels_target_id": null,
      "system_target_id": null,
      "system_campaign_id": 9872,
      "system_affiliate_id": null,
      "fired_pixels_count": 2,
      "charge_total": "0.04",
      "keys_pressed": null,
      "repeat": false,
      "affiliate_repeat": false,
      "target_repeat": null,
      "number_repeat": false,
      "visitor_url": "https://retreaver.com/users/sign_in",
      "company_id": 2,
      "conversions_determined_at": "2026-02-21T01:05:14.898Z",
      "updated_at": "2026-02-21T01:05:15.440Z",
      "created_at": "2026-02-21T01:04:15.975Z",
      "billable_minutes": 1,
      "upstream_call_uuid": null,
      "downstream_call_uuids": [],
      "target_group": {},
      "number": "+18884605668",
      "converted": false,
      "payable": false,
      "receivable": false,
      "conversion_seconds": null,
      "tid": null,
      "tags": {
        "attempt": "019c7db9-d309-e5e8-c2fe-450dab50a10d",
        "ga_client_id": "GA1.2.654836918.1748553244",
        "ga_session_id": "GS2.2.s1771629913$o299$g0$t1771629913$j60$l0$h0",
        "geo": "614,us,us-oh",
        "id": "019c7db9-d309-e5e8-c2fe-450dab50a10d",
        "request_id": "019c7db9-d309-e5e8-c2fe-450dab50a10d",
        "robodial_blacklist": "0",
        "status": "success"
      },
      "fired_pixels": [
        {
          "fired_pixel": {
            "url": "https://example.com/",
            "fire_order": 1,
            "batch_uuid": "71ff3113-f1d0-49e9-b344-86a7d1394600",
            "created_at": "2026-02-21T01:05:15.118Z",
            "fired_at": "2026-02-21T01:05:15.371Z",
            "status": "fired",
            "webhook_name": null
          }
        },
        {
          "fired_pixel": {
            "url": "https://hooks.zapier.com/hooks/catch/4588370/okv71k5/?from=%2B16146792390&to=%2B18884605668",
            "fire_order": 0,
            "batch_uuid": "dd4359de-9f77-4f95-b71a-541682911509",
            "created_at": "2026-02-21T01:04:22.081Z",
            "fired_at": "2026-02-21T01:04:16.147Z",
            "status": "fired",
            "webhook_name": "Robodial Scan and Filter"
          }
        }
      ],
      "via": "inbound-dial",
      "rescued": false
    }
  },
  {
    "call": {
      "uuid": "3df3c1fc-da38-439b-b637-80fd8978959d",
      "caller": "+15634223835",
      "caller_number_sent": null,
      "caller_zip": null,
      "caller_state": "IA",
      "caller_city": "WEST UNION",
      "caller_country": "US",
      "dialed_call_duration": 0,
      "total_duration": 36,
      "ivr_duration": 36,
      "hold_duration": 0,
      "status": "finished",
      "start_time": "2026-02-20T23:21:06.820Z",
      "forwarded_time": null,
      "end_time": "2026-02-20T23:21:43.837Z",
      "cid": "1",
      "afid": null,
      "sid": null,
      "dialed_number": null,
      "revenue": null,
      "payout": null,
      "postback_value": null,
      "network_sale_timer_fired": null,
      "affiliate_sale_timer_fired": null,
      "target_sale_timer_fired": null,
      "hung_up_by": "caller",
      "duplicate": false,
      "payable_duplicate": false,
      "receivable_duplicate": false,
      "callpixels_target_id": null,
      "system_target_id": null,
      "system_campaign_id": 9872,
      "system_affiliate_id": null,
      "fired_pixels_count": 2,
      "charge_total": "0.04",
      "keys_pressed": null,
      "repeat": false,
      "affiliate_repeat": false,
      "target_repeat": null,
      "number_repeat": false,
      "visitor_url": "https://retreaver.com/",
      "company_id": 2,
      "conversions_determined_at": "2026-02-20T23:22:07.074Z",
      "updated_at": "2026-02-20T23:22:07.745Z",
      "created_at": "2026-02-20T23:21:06.988Z",
      "billable_minutes": 1,
      "upstream_call_uuid": null,
      "downstream_call_uuids": [],
      "target_group": {},
      "number": "+18882761902",
      "converted": false,
      "payable": false,
      "receivable": false,
      "conversion_seconds": null,
      "tid": null,
      "tags": {
        "attempt": "019c7d5b-635d-6bbb-91e7-84294fe3f30b",
        "ga_client_id": "GA1.2.858226335.1769609217",
        "ga_session_id": "GS2.2.s1771625754$o5$g0$t1771625754$j60$l0$h0",
        "geo": "563,us,us-ia",
        "id": "019c7d5b-635d-6bbb-91e7-84294fe3f30b",
        "request_id": "019c7d5b-635d-6bbb-91e7-84294fe3f30b",
        "robodial_blacklist": "0",
        "status": "success"
      },
      "fired_pixels": [
        {
          "fired_pixel": {
            "url": "https://hooks.zapier.com/hooks/catch/4588370/okv71k5/?from=%2B15634223835&to=%2B18882761902",
            "fire_order": 0,
            "batch_uuid": "672ab5e7-ff5e-48f0-bdfa-42f910b1e731",
            "created_at": "2026-02-20T23:21:13.116Z",
            "fired_at": "2026-02-20T23:21:07.176Z",
            "status": "fired",
            "webhook_name": "Robodial Scan and Filter"
          }
        },
        {
          "fired_pixel": {
            "url": "https://example.com/",
            "fire_order": 1,
            "batch_uuid": "28710a61-38c1-44d8-8307-946d6aabe08c",
            "created_at": "2026-02-20T23:22:07.329Z",
            "fired_at": "2026-02-20T23:22:07.652Z",
            "status": "fired",
            "webhook_name": null
          }
        }
      ],
      "via": "inbound-dial",
      "rescued": false
    }
  }
]


### V2 - Get recent Calls

```bash
curl "https://api.retreaver.com/api/v2/calls.json?api_key=woofwoofwoof"
```

Provides access to the call log. The call log contains all the Calls which have been made through Numbers under your control.

#### What's new in V2?

In addition to all of the attributes that were returned by V1, this version also returns the following fields:

| attribute | Format | Description |
|-----------|--------|-------------|
| affiliate_name | `"abcdef"` | The full name of the affiliate that sent the call. |
| campaign_id | `123456` | The ID of the campaign the call was sent to. |
| campaign_name | `"abcdef"` | The name of the campaign the call was sent to. |
| connected | `true` or `false` | Whether the caller was successfully connected to a target. |
| number_id | `123456` | The ID of the number that the call was received on. |
| profit_gross | `0.00` | The gross profit on the call. Formula: `(revenue) - (payout) - (total cost)` |
| profit_net | `0.00` | The net profit on the call. Formula: `(revenue) - (payout)` |
| target_id | `123456` | The target that the caller was connected to. |
| target_name | `"John Doe"` | The full name of the target that the caller was connected to. |
| time_to_call_in_seconds | `10` | The time it took for the caller to actually make the call. |
| time_to_connect_in_seconds | `10` | The time it took for the caller to get connected to a buyer. Formula: `(IVR duration) + (hold duration)` |
| total_cost | `0.00` | The total cost of the call. |

#### HTTP Request

`GET https://api.retreaver.com/api/v2/calls.json?api_key=woofwoofwoof`

#### Query Parameters

| Parameter | Format | Default | Description |
|-----------|--------|---------|-------------|
| company_id | `123456` | | Return any Calls associated to the specific company IF you have access to that company. |
| created_at_start | `YYYY-MM-DDTHH:MM:SS+HH:MM` | -4712-01-01T00:00:00+00:00 | Return any Calls that were created after this date. |
| created_at_end | `YYYY-MM-DDTHH:MM:SS+HH:MM` | 4712-01-01T00:00:00+00:00 | Return any Calls that were created before this date. |
| sort_by | `created_at` or `updated_at` | `created_at` | Calls will be sorted by this value. |
| order | `asc` or `desc` | `desc` | Calls will be sorted in ascending or descending order. |
| caller | `%2B13015236555` | | Return only calls from the specified caller number. |
| client_afid | `123456` | | Return calls for an affiliate. |
| client_cid | `123456` | | Return calls for a specific campaign. |
| client_tid | `123456` | | Return calls for a specific target. |
| sub_id | `123456` | | Return calls for a affiliate Sub ID. |
| call_flow_events | true/false | false | Returns the call flow events of what happened during the call |

### V2 - Enumerate through all calls

First page:

```bash
curl "https://api.retreaver.com/api/v2/calls.json?api_key=woofwoofwoof&page=1"
```

Second page:

```bash
curl "https://api.retreaver.com/api/v2/calls.json?api_key=woofwoofwoof&page=2"
```

To fetch all Calls on your Account, use the `sort_by` and `order` params to return your Calls in the order they were created, and then paginate through all your calls.

#### HTTP Request

```
https://api.retreaver.com/api/v2/calls.json?api_key=woofwoofwoof&company_id=1&sort_by=created_at&order=asc&page=1
https://api.retreaver.com/api/v2/calls.json?api_key=woofwoofwoof&company_id=1&sort_by=created_at&order=asc&page=2
```

### V2 - Enumerate through Calls in a specific date/time range

```bash
curl "https://api.retreaver.com/calls.json?api_key=woofwoofwoof&company_id=1&created_at_start=2016-01-01T00:00:00+00:00&created_at_end=2016-01-02T00:00:00+00:00&page=1"
```

By passing in `created_at_start` and `created_at_end` parameters, you can control the start and end time of Calls returned.

#### HTTP Request

`GET https://api.retreaver.com/api/v2/calls.json?api_key=woofwoofwoof&company_id=1&created_at_start=2016-01-01T00:00:00+00:00&created_at_end=2016-01-02T00:00:00+00:00&page=1`

### V2 - Get a specific Call

```bash
curl "https://api.retreaver.com/api/v2/calls/94079290-93f3-4527-9e78-88653aaf3c49.json?api_key=woofwoofwoof"
```

Calls can be accessed by their UUID.

#### HTTP Request

`GET https://api.retreaver.com/api/v2/calls/addcf985-017e-4962-be34-cf5d55e74afc.json?api_key=woofwoofwoof&company_id=1`

### V3 - Calls

V3 follows the same behavior as V2. Refer to it for specific calls and usage. We recommend just using the V3 /calls API, as it will return the most information.

### Call Data Writing

Retreaver users can create data posting links that give publishers the ability to apply tags to an inbound caller using call data writing, these tags can be applied at any time, either before or after a call has been processed within a Retreaver campaign.

Call data writing is typically used when you need to apply tags to calls before connecting the caller to a campaign, or before transferring the call to another agent.

Check our guide: [Applying Tags to Calls using Call Data Writing](https://help.retreaver.com/hc/en-us/articles/360034356152-Publisher-Data-Posting-Applying-Tags-to-Calls-using-Call-Data-Writing)

#### Available on retreaverdata.com domain

Note that all requests must be made to **retreaverdata.com**.

#### Methods

Requests could be made through POST and GET

When using GET place the params in the URL

**GET:**

```bash
curl "https://reteaverdata.com/data_writing/:postback_key_uuid?caller_number=:caller_number&age=39&utm_campaign=auto"
```

**POST:**

```bash
curl -X POST "https://reteaverdata.com/data_writing" \
  -H "Content-Type: application/json" \
  -d '{
    "key": postback_key_uuid,
    "caller_number": :caller_number,
    "age": "39",
    "utm_campaign": "auto"
  }'
```

**Example Response with call_uuid:**

```json
{
  "tag_values": {
    "age":"39",
    "utm_campaign":"auto"
  },
  "call_uuid":"9b653cf0-4835-493b-860c-aed9b7af2a4a",
  "status":"completed call found, tags applied"
}
```

**Example Response with caller_number:**

```json
{
  "tag_values": {
    "age":"39",
    "utm_campaign":"auto"
  },
  "caller_number":"+3569878933094",
  "status":"call not found, tags stored"
}
```

#### HTTP Request

`POST/GET https://retreaverdata.com/data_writing`

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| key | string | Yes | The UUID of the Postback Key used to authorize this change |
| caller_number | string | Optional | The caller number of the Call for which the tags should be applied. This or a call_uuid should be provider |
| call_uuid | string | Optional | The uuid of the Call for which the tags should be applied. This or a caller_number should be provided. |
| :tag_key | string | Optional | Dynamic key:value pairs in the form of '?key1=value1&key2=value2' |

#### Call not found

The DataWriting API allows for tags to be sent before a call comes in. When the call is not found the tags are stored and will be applied when a call from the caller number is received.

#### Completed call found

When a call is found and is completed the tags are applied.

#### In progress call found

When a call is in progress, tags can be stored but may not be applied to the call immediately. Instead, they are typically applied the next time they are needed—usually when a routing decision must be made. If no further routing decisions occur while the call remains in progress, the tags are applied at the end of the call.

As a result, it's possible to use the Data Writing API to set tags on an in-progress call, but not see them immediately reflected in the UI or API. They may only become visible once the call has ended.

Note that if the call has already been routed, the tags will still be applied eventually—but since routing is complete, they will not influence the routing outcome.

---

## Affiliates

Entering Affiliates into our system allows you to attribute calls back to the Affiliate who created them, and to update any external tracking systems.

If you're not in affiliate marketing, Affiliate objects can be used for whatever source attribution is relevant. Affiliates exist for your reference.

### Get all Affiliates

```bash
curl "https://api.retreaver.com/affiliates.xml?api_key=woofwoofwoof&company_id=1"
```

The above command returns XML structured like this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<affiliates type="array">
  <affiliate>
    <afid>0002</afid>
    <first-name>Nancy</first-name>
    <last-name>Drew</last-name>
    <company-name>Acme</last-name>
    <updated-at type="datetime">2012-05-03T15:56:01Z</updated-at>
    <created-at type="datetime">2012-05-03T15:56:01Z</created-at>
  </affiliate>
</affiliates>
```

Provides a complete list of Affiliates.

#### HTTP Request

`GET https://api.retreaver.com/affiliates.xml?api_key=woofwoofwoof&company_id=1`

### Get a specific Affiliate by your ID

```bash
curl "https://api.retreaver.com/affiliates/afid/0002.json?api_key=woofwoofwoof&company_id=1"
```

Finds an Affiliate by AFID.

#### HTTP Request

`GET https://api.retreaver.com/affiliates/afid/0002.xml?api_key=woofwoofwoof&company_id=1`

### Create an Affiliate

```bash
curl -s \
    -X POST \
    https://api.retreaver.com/affiliates.json?api_key=woofwoofwoof&company_id=1 \
    -H "Content-Type: application/json" \
    -d '{"affiliate":{"first_name":"Nancy", "last_name":"Drew", "afid":"0002"}}'
```

Creates an Affiliate.

#### HTTP Request

`POST https://api.retreaver.com/affiliates.json?api_key=woofwoofwoof&company_id=1`

`Content-Type: application/json`

`{"affiliate":{"first_name":"Nancy", "last_name":"Drew", "afid":"0002"}}`

#### Parameters

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| afid | string | null | required | The affiliate's ID. This should align with any external tracking systems you may be using. |
| first_name | string | null | | The affiliate's first name, for your reference. |
| last_name | string | null | | Their last name. |
| company_name | string | null | | Their company name. |

### Update an Affiliate

```bash
curl -s \
    -X PUT \
    https://api.retreaver.com/affiliates/afid/002.json \
    -H "Content-Type: application/json" \
    -d '{"affiliate":{"first_name":"Nathan"}}'
```

The above command returns JSON structured like this:

```json
{
  "affiliate": {
    "afid": "002",
    "first_name": "Nathan",
    "last_name": "Drew",
    "company_name": null,
    "updated_at": "2012-05-03T20:20:03Z",
    "created_at": "2012-05-03T14:29:37Z"
  }
}
```

Changes any attributes you have passed in on the Affiliate.

You must replace `0002` with the afid of the Affiliate you want to delete.

#### HTTP Request

`PUT https://api.retreaver.com/affiliates/afid/0002.json?api_key=woofwoofwoof&company_id=1`

`Content-Type: application/json`

`{"affiliate":{"first_name":"Nathan"}}`

### Remove an affiliate

```bash
curl -X DELETE https://api.retreaver.com/affiliates/afid/0002.json?api_key=woofwoofwoof&company_id=1
```

Deletes the given Affiliate. You must delete any Numbers the Affiliate has before deleting the Affiliate.

---

## Targets

Targets are the destination phone numbers that calls are routed to, for instance, your call center.

### Get all Targets

```bash
curl "https://api.retreaver.com/targets.json?api_key=woofwoofwoof&company_id=1"
```

The above command returns JSON structured like this:

```json
[{
   "target": {
     "id": 6588,
     "number": "+18668987878",
     "sip_username": null,
     "sip_password": null,
     "cid_number_id": 10,
     "obfuscate_cid": false,
     "created_at": "2014-08-14T20:46:01.158-04:00",
     "updated_at": "2016-06-28T13:02:52.964-04:00",
     "object_key": "40a9a73ff97cb35a0a16d1ec89fd9eddcf3727df932cea9f0f7a5a8ba1684fed",
     "tid": null,
     "priority": 1,
     "weight": 1,
     "timeout_seconds": 15,
     "timer_offset": 0,
     "send_digits": null,
     "concurrency_cap": null,
     "calls_in_progress": 0,
     "inband_signals": false,
     "time_zone": "Eastern Time (US & Canada)",
     "paused": false,
     "paused_at": null,
     "name": "Jason Cell"
   }
}]
```

#### HTTP Request

`GET https://api.retreaver.com/targets.json?api_key=woofwoofwoof&company_id=1`

### Get a specific Target

```bash
curl "https://api.retreaver.com/targets/6588.json?api_key=woofwoofwoof&company_id=1"
```

The above command returns JSON structured like this:

```json
{
   "target": {
     "id": 6588,
     "number": "+18668987878",
     "sip_username": null,
     "sip_password": null,
     "cid_number_id": 10,
     "obfuscate_cid": false,
     "created_at": "2014-08-14T20:46:01.158-04:00",
     "updated_at": "2016-06-28T13:02:52.964-04:00",
     "object_key": "40a9a73ff97cb35a0a16d1ec89fd9eddcf3727df932cea9f0f7a5a8ba1684fed",
     "tid": null,
     "priority": 1,
     "weight": 1,
     "timeout_seconds": 15,
     "timer_offset": 0,
     "send_digits": null,
     "concurrency_cap": null,
     "calls_in_progress": 0,
     "inband_signals": false,
     "time_zone": "Eastern Time (US & Canada)",
     "paused": false,
     "paused_at": null,
     "name": "Jason Cell"
   }
}
```

#### HTTP Request

`GET https://api.retreaver.com/targets/6588.json?api_key=woofwoofwoof&company_id=1`

### Create a Target

```bash
curl -s \
 -X POST \
 https://api.retreaver.com/targets.json?api_key=woofwoofwoof&company_id=1 \
 -H "Content-Type: application/json" \
 -d '{"target":{"number":"+18668987878", "name":"Retreaver Support"}}'
```

Creates a new Target.

#### HTTP Request

`POST https://api.retreaver.com/targets.json?api_key=woofwoofwoof&company_id=1`

`Content-Type: application/json`

`{"target":{"number":"+18668987878", "name":"Retreaver Support"}}`

#### Parameters

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| name | string | | | A descriptive moniker for this target so you'll know what it is. |
| number | string | | required | Either a phone number or `sip:user@domain.com` formatted SIP endpoint. PSTN numbers should be [E.164 formatted](https://en.wikipedia.org/wiki/E.164). |
| sip_username | string | | | The SIP username, if using SIP-authentication to call a SIP endpoint. |
| sip_password | string | | | The SIP password, if using SIP-authentication to call a SIP endpoint. |
| tid | string | | | Your own internal ID for this target. |
| priority | integer | 1 | | The target with the lowest priority value gets considered first when routing calls to a set of targets. |
| weight | integer | 1 | | When more than one target has the same priority, the cumulative weight of the targets being considered is used to randomize their order. |
| timeout_seconds | integer | 30 | | The maximum number of seconds we'll wait while the target number is ringing before moving on. |
| inband_signals | boolean | false | | Enables detection of in-band ringing in conjunction with `timer_offset`. |
| timer_offset | integer | 0 | | Offsets any timers on Tracking URLs or Conversion Criteria when routing to this target. |
| send_digits | string | | | Send these digits as DTMF tones when the call recipient picks up. Use `w` to make a 0.5 second pause. |
| concurrency_cap | integer | null | | Used to limit the maximum number of concurrent calls a target can receive. |
| paused | boolean | false | | Targets which are paused will not be considered when routing calls. |
| time_zone | string | UTC | | The time zone used when determining if a call is occuring during business hours. |
| business_hours_attributes | array | | | An optional array of business hours. |

### Update a Target

```bash
curl -s \
 -X PUT \
 https://api.retreaver.com/targets/22592.json \
 -H "Content-Type: application/json" \
 -d '{"target":{"paused":true}}'
```

Changes any attributes you have passed in on the Target.

#### HTTP Request

`PUT https://api.retreaver.com/targets/22592.json?api_key=woofwoofwoof&company_id=1`

`Content-Type: application/json`

`{"target":{"paused":true}}`

### Remove a Target

```bash
curl -X DELETE https://api.retreaver.com/targets/22592.json?api_key=woofwoofwoof&company_id=1
```

Deletes the given Target.

#### HTTP Request

`DELETE https://api.retreaver.com/targets/22592.json?api_key=woofwoofwoof&company_id=1`

### Tagging a Target

```bash
curl -s \
 -X PUT \
 https://api.retreaver.com/targets/22592.json \
 -H "Content-Type: application/json" \
 -d '{"target":{"tag_list":"<<<calling_about:support>>>,<<<calling_about:other>>>"}}'
```

To set tags on a Target, pass in a comma delineated, triple-angle-bracket enclosed string of tags as the `tag_list` value.

The system will create/find whatever tags you have set given this input without you having to track tag IDs. You must include the full list of tags you want set any time a tag_list parameter is passed in. To clear the tags, just pass in a blank string.

There is a limit of 100 tags added in this manner, but the system will automatically concatenate US zip `geo` tags.

#### HTTP Request

`PUT https://api.retreaver.com/targets/22592.json?api_key=woofwoofwoof&company_id=1`

`Content-Type: application/json`

`{"target":{"tag_list":"<<<calling_about:support>>>,<<<calling_about:other>>>"}}`

### Changing a Target's Caps

```bash
curl -s \
 -X PUT \
 https://api.retreaver.com/targets/22592.json \
 -H "Content-Type: application/json" \
 -d '{"target": { "hard_cap_attributes": { "cap": 100 } } }'
```

There are 4 types of caps: Hard Cap, Hourly Cap, Daily Cap, and Monthly Cap. Hard cap is a hard limit, and once it is reached, the target will not receive more Calls until the Cap is reset. This is useful when routing Calls to buyers that have insertion orders for a set number of leads.

The other types of Cap reset periodically as expected.

You can modify these Caps by updating your Target with nested objects `hard_cap_attributes`, `hourly_cap_attributes`, `daily_cap_attributes`, and `monthly_cap_attributes`.

#### HTTP Request

`PUT https://api.retreaver.com/targets/22592.json?api_key=woofwoofwoof&company_id=1`

`Content-Type: application/json`

`{"target":{"hard_cap_attributes":{"cap":100}}}`

#### Parameters

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| cap | integer | | required | The value for the cap. |

### Resetting a Hard Cap

```bash
curl -s \
 -X POST \
 https://api.retreaver.com/targets/22592/reset_cap.json?api_key=woofwoofwoof&company_id=1 \
 -H "Content-Type: application/json"
```

Clears any Calls contributing to the given Target's hard cap, resetting it to 0. Returns HTTP 200 on success.

#### HTTP Request

`POST https://api.retreaver.com/targets/22592/reset_cap.json?api_key=woofwoofwoof&company_id=1`

`Content-Type: application/json`

---

## Campaigns

By configuring a Campaign, you can reuse the settings of the Campaign when creating Numbers. Campaigns should be configured before creating Numbers.

### Get all Campaigns

```bash
curl "https://api.retreaver.com/campaigns.json?api_key=woofwoofwoof&company_id=1"
```

List all the Campaigns in your Account.

#### HTTP Request

`GET https://api.retreaver.com/campaigns.json?api_key=woofwoofwoof&company_id=1`

### Get a specific Campaign

```bash
curl "https://api.retreaver.com/campaigns/cid/0044.json?api_key=woofwoofwoof&company_id=1"
```

Get a campaign by your ID.

#### HTTP Request

`GET https://api.retreaver.com/campaigns/cid/0044.json?api_key=woofwoofwoof&company_id=1`

### Create a Campaign

```bash
curl -s \
    -X POST \
    https://api.retreaver.com/campaigns.json \
    -H "Content-Type: application/json" \
    -d '{ \
            "campaign": { \
                "cid": "000333", \
                "name": "MyCampaign", \
                "message": "Thanks for calling, please press one to continue.", \
                "voice_gender": "Male", \
                "timers_attributes": [{ \
                    "seconds": 0, \
                    "url": "http://callpixels.com/click.html" \
                }, { \
                    "seconds": 90, \
                    "url": "http://callpixels.com/sale.html" \
                }], \
                "menu_options_attributes": [{ \
                    "option": "1", \
                    "target_number": "+16474570424" \
                   } \
                ] \
            } \
        }'
```

Create a new Campaign.

For Extensive Campaign Creation, here is the -d payload/body. This includes adding a target to the campaign, for example.

{
  "campaign": {
    "repeat_caller_type": "normal",
    "name": "",
    "client_cid": "",
    "alternative_id": "",
    "record_seconds": "",
    "menu_options_attributes": {
      "86241": {
        "id": 86241,
        "_destroy": false,
        "action": 1,
        "options": [],
        "menu_options_targets_attributes": {
          "361700": {
            "id": 361700,
            "_destroy": false,
            "menu_option_id": 86241,
            "target_id": "",
            "target_group_id": "",
            "disabled": false,
            "rescue_enabled": true,
            "priority": "",
            "weight": "",
            "locked": false,
            "enable_route_by_bid": false,
            "enable_route_by_performance": false,
            "performance": "",
            "performance_lookback_period_value": "",
            "performance_type": "",
            "min_calls_required": "",
            "default_performance": "",
            "enable_route_by_state_performance": false
          },
          "361701": {
            "id": 361701,
            "_destroy": false,
            "menu_option_id": 86241,
            "target_id": "",
            "target_group_id": "",
            "disabled": false,
            "rescue_enabled": true,
            "priority": "",
            "weight": "",
            "locked": true,
            "enable_route_by_bid": false,
            "enable_route_by_performance": false,
            "performance": "",
            "performance_lookback_period_value": "",
            "performance_type": "",
            "min_calls_required": "",
            "default_performance": "",
            "enable_route_by_state_performance": false
          },
          "361702": {
            "id": 361702,
            "_destroy": false,
            "menu_option_id": 86241,
            "target_id": "",
            "target_group_id": "",
            "disabled": false,
            "rescue_enabled": true,
            "priority": "",
            "weight": "",
            "locked": true,
            "enable_route_by_bid": false,
            "enable_route_by_performance": false,
            "performance": "",
            "performance_lookback_period_value": "",
            "performance_type": "",
            "min_calls_required": "",
            "default_performance": "",
            "enable_route_by_state_performance": false
          },
          "1987894144": {
            "menu_option_id": 86241,
            "target_id": "",
            "target_group_id": "",
            "disabled": false,
            "rescue_enabled": true,
            "priority": "",
            "weight": "",
            "locked": true,
            "enable_route_by_bid": false,
            "enable_route_by_performance": false,
            "performance": "",
            "performance_lookback_period_value": "",
            "performance_type": "",
            "min_calls_required": "",
            "default_performance": "",
            "enable_route_by_state_performance": false
          }
        }
      }
    },
    "conversion_groups_attributes": {
      "0": {
        "id": 237410,
        "_destroy": false,
        "eval_order": "",
        "conversion_type": "",
        "name": "",
        "dedupe_seconds": "",
        "tag_list": "",
        "secondary_tag_list": "",
        "conversions_attributes": {
          "0": {
            "_destroy": false,
            "id": 243778,
            "conversion_type": "",
            "postback_timeout": "",
            "match_trigger": "",
            "seconds": "",
            "revenue": "",
            "payout": "",
            "payout_percent": false,
            "payout_modifier": "",
            "seconds_tag": "",
            "revenue_tag": "",
            "payout_tag": "",
            "payable_seconds_modifier": ""
          }
        }
      },
      "1": {
        "id": 237411,
        "_destroy": false,
        "eval_order": "",
        "conversion_type": "",
        "dedupe_seconds": "",
        "secondary_tag_list": "",
        "conversions_attributes": {
          "0": {
            "_destroy": false,
            "id": 243779,
            "conversion_type": "",
            "postback_timeout": "",
            "match_trigger": "",
            "seconds": "",
            "revenue": "",
            "payout": "",
            "payout_percent": false,
            "payout_modifier": "",
            "seconds_tag": "",
            "revenue_tag": "",
            "payout_tag": "",
            "payable_seconds_modifier": ""
          }
        }
      }
    }
  }
}

#### HTTP Request

`POST https://api.retreaver.com/campaigns.json?api_key=woofwoofwoof&company_id=1`

`Content-Type: application/json`

#### Campaign Creation Parameters

The example request for campaign creation covers plenty.

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| cid | string | Random 8 characters | | Your internal campaign ID that will be referenced in the future. |
| name | string | | | A name for the campaign for your reference. |
| dedupe_seconds | integer | 0 (Disabled) | | Prevent a repeat caller from causing any Connect or Sale timer from firing within n seconds. |
| affiliate_can_pull_number | boolean | false | | Allow affiliates to access this campaign via our LinkTrust integration. |
| record_calls | boolean | true | | Toggles call recording on and off. |
| message | string | | | Text-to-speech message read aloud to the caller when they dial your number. |
| voice_gender | string | Male | | Male or Female, the gender of the text-to-speech voice you want. |
| message_file | file | | | Audio file you would like played for the caller when they dial your number. |
| repeat | integer | 4 | | The number of times to repeat the greeting. |
| timers_attributes | array | | | An array of timers. |
| menu_option_attributes | array | | | An array of menu options. |

### Update a Campaign

```bash
curl -s \
    -X PUT \
    https://api.retreaver.com/campaigns/cid/0044.json \
    -H "Content-Type: application/json" \
    -d '{"campaign":{"name":"My Other Campaign"}}'
```

Changes any attributes you have passed in on the Campaign.

You must replace `0044` with the cid of the Campaign you want to update.

### Adding general webhooks to a campaign

In order to add a webhook to a campaign, the request below works:

POST https://api.retreaver.com/campaigns/CID/timers?api_key=woofwoofwoof&company_id=1

{
  "start_timer": {
    "id": "",
    "_destroy": false,
    "trigger_type": ,
    "name": "",
    "dedupe_seconds": 0,
    "tag_list": "",
    "pixels_attributes": {
      "0": {
        "_destroy": false,
        "id": "",
        "fire_order": 0,
        "request_method": "post",
        "url": "https://webhookurl.com",
        "wcf_template_id": "",
        "wcf_target_id": ""
      }
    }
  },
  "wcf_output_tag_prefix_field": "",
  "wcf_ping_url_field": "",
  "wcf_ping_method_field": "POST",
  "wcf_ping_headers_field": "",
  "wcf_ping_data_field": "",
  "wcf_ping_output_map_field": "",
  "wcf_post_condition_key_field": "",
  "wcf_post_condition_operator_field": "is_greater_than",
  "wcf_post_condition_value_field": "",
  "wcf_post_url_field": "",
  "wcf_post_method_field": "POST",
  "wcf_post_headers_field": "",
  "wcf_post_data_field": "",
  "wcf_post_output_map_field": "",
  "wcf_payout_output_tag_field": "",
  "wcf_payout_modifier_multiplier_field": "",
  "wcf_revenue_output_tag_field": "",
  "wcf_revenue_modifier_multiplier_field": "",
  "wcf_timer_offset_tag_field": "",
  "wcf_timer_offset_modifier_field": "",
  "update_buyer_tags": ""
}

For the trigger_type attribute of the webhook payload, which is required, use the following mapping:

When a call comes in/starts, trigger_type:9
when a call is converted, trigger_type:5
for a passthrough webhooks, when someone is brokering with both rtb publishers and buyers, trigger_type:12
for data appending webhooks, trigger_type:13

### Creating an RTB url for your affiliates/publishers

The request below creates the rtb url to provide to your publishers

POST https://api.retreaver.com/campaigns/1147/postback_keys?api_key=woofwoofwoof&company_id=1

{
  "postback_key": {
    "action": "rtb",
    "name": "",
    "tag_prefix": "",
    "ttl_seconds": 30,
    "timeout": 3.0,
    "inbound_number": "",
    "return_dba": 0,
    "add_to_caps_on_status_reserved": 0,
    "route_only_to_reserved_target": 0,
    "allow_no_caller_number": 0,
    "paused": 0,
    "claim_percent_threshold": 10,
    "blocked_inbound_percent": 50,
    "ping_shield_outbound_count_limit": "",
    "ping_shield_outbound_ms_limit": ""
  }
}

### Adding webhooks using the webhook configurator preset template

For example, the request below makes an RTB webhook for a ringba buyer, using the webhook configurator:

POST https://api.retreaver.com/campaigns/1147/timers?api_key=woofwoofwoof&company_id=1

{
  "passthrough_timer": {
    "id": "",
    "_destroy": false,
    "trigger_type": 12,
    "name": "config",
    "dedupe_seconds": 0,
    "tag_list": "",
    "pixels_attributes": {
      "0": {
        "_destroy": false,
        "id": "",
        "fire_order": 0,
        "request_method": "post",
        "url": "https://retreaver.com/webhook-configurator/v1/?call_key=[call_key]&call_uuid=[call_uuid]&output_tag_prefix=ringba_125879&ping_url=https://rtb.ringba.com/v1/production/98765.json&ping_method=POST&ping_headers={\"Content-Type\":\"application/json\"}&ping_data={\"CID\":\"[nanp_caller_number]\",\"state\":\"[caller_state]\",\"zipCode\":\"[caller_zip]\",\"exposeCallerId\":\"yes\"}&ping_output_map={\"PingOutputMap\":{\"number\":\"phoneNumber\",\"bid\":\"bidAmount\",\"timer\":\"bidTerms[0].callMinDuration\"}}",
        "wcf_template_id": "ringba_rtb_ping_post",
        "wcf_target_id": 125879
      }
    }
  },
  "wcf_output_tag_prefix_field": "ringba_12345",
  "wcf_ping_url_field": "https://rtb.ringba.com/v1/production/TEMPLATE_RTB_ID.json",
  "wcf_ping_method_field": "POST",
  "wcf_ping_headers_field": "{\"Content-Type\":\"application/json\"}",
  "wcf_ping_data_field": "{\"CID\":\"[nanp_caller_number]\",\"state\":\"[caller_state]\",\"zipCode\":\"[caller_zip]\",\"exposeCallerId\":\"yes\"}",
  "wcf_ping_output_map_field": "{\"PingOutputMap\":{\"number\":\"phoneNumber\",\"bid\":\"bidAmount\",\"timer\":\"bidTerms[0].callMinDuration\"}}",
  "wcf_post_condition_key_field": "",
  "wcf_post_condition_value_field": "",
  "wcf_post_url_field": "",
  "wcf_post_headers_field": "",
  "wcf_post_data_field": "",
  "wcf_post_output_map_field": "",
  "wcf_payout_output_tag_field": "",
  "wcf_payout_modifier_multiplier_field": "",
  "wcf_revenue_output_tag_field": "",
  "wcf_revenue_modifier_multiplier_field": "",
  "wcf_timer_offset_tag_field": "",
  "wcf_timer_offset_modifier_field": "",
  "update_buyer_tags": ""
}

It should be noted for the above request to work, that the target (in this case target that uses ringba) must already be placed in the campaign.

#### HTTP Request

`PUT https://api.retreaver.com/campaigns/cid/0044.json?api_key=woofwoofwoof&company_id=1`

`Content-Type: application/json`

`{"campaign":{"name":"My Other Campaign"}}`

### Remove a Campaign

```bash
curl -X DELETE https://api.retreaver.com/campaigns/cid/0044.json?api_key=woofwoofwoof&company_id=1
```

Delete a Campaign by CID. You must delete all the Numbers belonging to that Campaign first.

---

## Numbers

Numbers are the physical phone numbers that you want routed to a Campaign. A Number can be routed directly to the Target phone number, or it can be screened with a greeting which requires the caller to press a button to continue.

Numbers can be set to use the settings of an existing Campaign.

### Get all Numbers

```bash
curl "https://api.retreaver.com/numbers.json?api_key=woofwoofwoof&company_id=1"
```

Get all Numbers belonging to the Company.

#### HTTP Request

`GET https://api.retreaver.com/numbers.json?api_key=woofwoofwoof&company_id=1`

### Get a specific Number

```bash
curl "https://api.retreaver.com/numbers/5.json?api_key=woofwoofwoof&company_id=1"
```

Get a Number by our internal ID.

#### HTTP Request

`GET https://api.retreaver.com/numbers/5.json?api_key=woofwoofwoof&company_id=1`

### Create a Number

```bash
curl -s \
    -X POST \
    https://api.retreaver.com/numbers.json \
    -H "Content-Type: application/json" \
    -d '{"number":{"type":"Toll-free","desired_text":"TEST","afid":"0002","cid":"0001","sid":"superaffiliate"}}'
```

Creates a new phone Number.

#### HTTP Request

`POST https://api.retreaver.com/numbers.json?api_key=woofwoofwoof&company_id=1`

`Content-Type: application/json`

#### Parameters

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| type | string | Toll-free | required | Toll-free or Local, the kind of number that is desired. |
| desired_text | string | | | If you would like us to attempt to get a number that contains a specific word, enter it here. |
| country | string | US | | For Local numbers only, the 2 character country code for the country you would like the number to be in. |
| afid | string | | required | The affiliate ID this number belongs to. If not found, we will create a new affiliate with this AFID. |
| cid | string | | required | The campaign ID this number belongs to. You must set up the campaign before creating a number for it. |
| sid | string | | | The SubID this number belongs to. |

### Update a Number

```bash
curl -s \
    -X PUT \
    https://api.retreaver.com/numbers/79.json?api_key=woofwoofwoof&company_id=1 \
    -H "Content-Type: application/json" \
    -d '{"number":{"afid":"0005"}}'
```

Updates the Number with any attributes you have passed in.

#### HTTP Request

`PUT https://api.retreaver.com/numbers/79.json?api_key=woofwoofwoof&company_id=1`

`Content-Type: application/json`

`{"number":{"afid":"0005"}}`

### Remove a Number

```bash
curl -X DELETE https://api.retreaver.com/numbers/79.json?api_key=woofwoofwoof&company_id=1
```

Deletes the given number. Numbers will be deprovisioned within 24 hours.

---

## Number Pools

Number Pools are used to dynamically assign Numbers whenever a user visits your website. Number Pools are used in lieu of static Numbers when you want to track many different attributes.

### Get all Number Pools

```bash
curl "https://api.retreaver.com/number_pools.json?api_key=woofwoofwoof&company_id=1"
```

Returns all the Number Pools you have in our system.

#### HTTP Request

`GET https://api.retreaver.com/number_pools.json?api_key=woofwoofwoof&company_id=1`

### Get a specific Number Pool

```bash
curl "https://api.retreaver.com/number_pools/1.json?api_key=woofwoofwoof&company_id=1"
```

Returns a single Number Pool based on our internal ID.

#### HTTP Request

`GET https://api.retreaver.com/number_pools/1.json?api_key=woofwoofwoof&company_id=1`

### Create a Number Pool

```bash
curl -s \
    -X POST \
    https://api.retreaver.com/number_pools.json?api_key=woofwoofwoof&company_id=1 \
    -H "Content-Type: application/json" \
    -d '{ \
            "number_pool": { \
                "cid": "111", \
                "max_pool_size": 100, \
                "hide_embedded_access": true, \
                "google_analytics": true \
            } \
        }'
```

Creates a new Number Pool.

#### HTTP Request

`POST https://api.retreaver.com/number_pools.json?api_key=woofwoofwoof&company_id=1`

`Content-Type: application/json`

#### Parameters

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| cid | string | | required | The campaign ID this number pool belongs to. |
| type | string | Toll-free | | Toll-free or Local, the type of number that is desired for this number pool. |
| country | string | US | | For Local number pools only, the 2 character country code. |
| afid | string | | | The affiliate ID this number pool belongs to. |
| max_pool_size | integer | 10 | | The maximum number of numbers you want in this number pool. |
| buffer_seconds | integer | 0 | | The number of seconds for a number to retain its assignment after the visitor has left your site. |
| hide_embedded_access | boolean | false | | When true, will not show the embedded affiliate phone number management interface for this campaign. |
| google_analytics | boolean | false | | Enables our Google Analytics integration. |
| reserve_size | integer | 1 | | The number of numbers to pre-provision and hold in reserve. |

### Update a Number Pool

```bash
curl -s \
    -X PUT \
    https://api.retreaver.com/number_pools/49.json \
    -H "Content-Type: application/json" \
    -d '{"number_pool":{"max_pool_size":"1000"}}'
```

Updates the Number Pool with any attributes you have passed in.

#### HTTP Request

`PUT https://api.retreaver.com/number_pools/49.json?api_key=woofwoofwoof&company_id=1`

`Content-Type: application/json`

`{"number_pool":{"max_pool_size":"1000"}}`

### Remove a Number Pool

```bash
curl -X DELETE https://api.retreaver.com/number_pools/49.json?api_key=woofwoofwoof&company_id=1
```

Deletes the given Number Pool. This will also delete all Numbers associated with this Number Pool!

---

## Create Tags

POST
https://retreaver.com/tags?api_key=woofwoofwoof&company_id=1

{
  "tag": {
    "key": "",
    "color": "",
    "values_report": 0,
    "type": "String",
    "prompt_enabled": false,
    "prompt_attributes": {
      "action": "undefined",
      "copy_message_file_from_id": "",
      "preset": "",
      "repeat": 0,
      "tts": "",
      "tts_gender": "Female",
      "tts_language": "en-US",
      "use_message_file": false
    }
  }
}

## Companies

Company exists to allow resellers to separate their resources by Company. AFID and CID collisions will not occur between Companies.

### Get the active Company

```bash
curl "https://api.retreaver.com/company.json?api_key=woofwoofwoof"
```

Returns the currently active Company. This is the Company that will be modified if a request is sent in without a specific company_id.

You should always pass in the `company_id` parameter when requesting other objects, because switching Companies in the web interface will also switch Companies in the API.

#### HTTP Request

`GET https://api.retreaver.com/company.json?api_key=woofwoofwoof`

### Get a specific Company

```bash
curl "https://api.retreaver.com/companies/1.json?api_key=woofwoofwoof"
```

#### HTTP Request

`GET https://api.retreaver.com/companies/1.json?api_key=woofwoofwoof`
