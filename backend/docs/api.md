# API Documentation

## Overview

This document provides documentation for the LADR English backend API.

## Authentication

All API endpoints require authentication using a Bearer token in the Authorization header:

```
Authorization: Bearer <your-token>
```

## Endpoints

### Auth

#### Verify Token
- **URL**: `/api/v1/verify`
- **Method**: `GET`
- **Description**: Verify the authentication token
- **Response**: 
  ```json
  {
    "ok": true,
    "token": "your-token"
  }
  ```

### Items (Words)

#### Create Item
- **URL**: `/api/v1/items`
- **Method**: `POST`
- **Description**: Create a new vocabulary item
- **Request Body**:
  ```json
  {
    "text": "example",
    "definition": "a representative form or pattern",
    "source": "dictionary"
  }
  ```
- **Response**: Returns the created item

#### List Items
- **URL**: `/api/v1/items`
- **Method**: `GET`
- **Description**: List vocabulary items with optional search and pagination
- **Query Parameters**:
  - `q`: Search keyword in text
  - `skip`: Number of items to skip (default: 0)
  - `limit`: Number of items to return (default: 50, max: 200)
- **Response**: Returns a list of items

#### Get Item
- **URL**: `/api/v1/items/{item_id}`
- **Method**: `GET`
- **Description**: Get a specific vocabulary item by ID
- **Response**: Returns the requested item

#### Update Item
- **URL**: `/api/v1/items/{item_id}`
- **Method**: `PUT`
- **Description**: Update a specific vocabulary item
- **Request Body**: Same as create item
- **Response**: Returns the updated item

#### Delete Item
- **URL**: `/api/v1/items/{item_id}`
- **Method**: `DELETE`
- **Description**: Delete a specific vocabulary item
- **Response**: 
  ```json
  {
    "ok": true
  }
  ```

#### Review Item
- **URL**: `/api/v1/items/{item_id}/review`
- **Method**: `POST`
- **Description**: Record a review for a vocabulary item
- **Request Body**:
  ```json
  {
    "quality": 4
  }
  ```
- **Response**: Returns the updated item

### Statistics

#### Get Statistics
- **URL**: `/api/v1/stats`
- **Method**: `GET`
- **Description**: Get statistics about the vocabulary items
- **Response**:
  ```json
  {
    "total": 100,
    "reviewed": 75,
    "due_today": 25
  }
  ```