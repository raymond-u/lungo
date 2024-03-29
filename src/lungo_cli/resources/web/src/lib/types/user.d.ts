/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run json-schema-to-typescript to regenerate this file.
 */

export type Username = string
export type Email = string
export type FirstName = string
export type LastName = string

export interface User {
    traits?: {
        username: Username
        email: Email
        name: {
            first: FirstName
            last: LastName
        }
    }
}
