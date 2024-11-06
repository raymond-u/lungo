/**
 * This file was auto-generated by openapi-typescript.
 * Do not make direct changes to the file.
 */

export interface paths {
    "/admin/relation-tuples": {
        parameters: {
            query?: never
            header?: never
            path?: never
            cookie?: never
        }
        get?: never
        /**
         * Create a Relationship
         * @description Use this endpoint to create a relationship.
         */
        put: operations["createRelationship"]
        post?: never
        /**
         * Delete Relationships
         * @description Use this endpoint to delete relationships
         */
        delete: operations["deleteRelationships"]
        options?: never
        head?: never
        /**
         * Patch Multiple Relationships
         * @description Use this endpoint to patch one or more relationships.
         */
        patch: operations["patchRelationships"]
        trace?: never
    }
    "/health/alive": {
        parameters: {
            query?: never
            header?: never
            path?: never
            cookie?: never
        }
        /**
         * Check HTTP Server Status
         * @description This endpoint returns a HTTP 200 status code when Ory Keto is accepting incoming
         *     HTTP requests. This status does currently not include checks whether the database connection is working.
         *
         *     If the service supports TLS Edge Termination, this endpoint does not require the
         *     `X-Forwarded-Proto` header to be set.
         *
         *     Be aware that if you are running multiple nodes of this service, the health status will never
         *     refer to the cluster state, only to a single instance.
         */
        get: operations["isAlive"]
        put?: never
        post?: never
        delete?: never
        options?: never
        head?: never
        patch?: never
        trace?: never
    }
    "/health/ready": {
        parameters: {
            query?: never
            header?: never
            path?: never
            cookie?: never
        }
        /**
         * Check HTTP Server and Database Status
         * @description This endpoint returns a HTTP 200 status code when Ory Keto is up running and the environment dependencies (e.g.
         *     the database) are responsive as well.
         *
         *     If the service supports TLS Edge Termination, this endpoint does not require the
         *     `X-Forwarded-Proto` header to be set.
         *
         *     Be aware that if you are running multiple nodes of Ory Keto, the health status will never
         *     refer to the cluster state, only to a single instance.
         */
        get: operations["isReady"]
        put?: never
        post?: never
        delete?: never
        options?: never
        head?: never
        patch?: never
        trace?: never
    }
    "/namespaces": {
        parameters: {
            query?: never
            header?: never
            path?: never
            cookie?: never
        }
        /**
         * Query namespaces
         * @description Get all namespaces
         */
        get: operations["listRelationshipNamespaces"]
        put?: never
        post?: never
        delete?: never
        options?: never
        head?: never
        patch?: never
        trace?: never
    }
    "/opl/syntax/check": {
        parameters: {
            query?: never
            header?: never
            path?: never
            cookie?: never
        }
        get?: never
        put?: never
        /**
         * Check the syntax of an OPL file
         * @description The OPL file is expected in the body of the request.
         */
        post: operations["checkOplSyntax"]
        delete?: never
        options?: never
        head?: never
        patch?: never
        trace?: never
    }
    "/relation-tuples": {
        parameters: {
            query?: never
            header?: never
            path?: never
            cookie?: never
        }
        /**
         * Query relationships
         * @description Get all relationships that match the query. Only the namespace field is required.
         */
        get: operations["getRelationships"]
        put?: never
        post?: never
        delete?: never
        options?: never
        head?: never
        patch?: never
        trace?: never
    }
    "/relation-tuples/check": {
        parameters: {
            query?: never
            header?: never
            path?: never
            cookie?: never
        }
        /**
         * Check a permission
         * @description To learn how relationship tuples and the check works, head over to [the documentation](https://www.ory.sh/docs/keto/concepts/api-overview).
         */
        get: operations["checkPermissionOrError"]
        put?: never
        /**
         * Check a permission
         * @description To learn how relationship tuples and the check works, head over to [the documentation](https://www.ory.sh/docs/keto/concepts/api-overview).
         */
        post: operations["postCheckPermissionOrError"]
        delete?: never
        options?: never
        head?: never
        patch?: never
        trace?: never
    }
    "/relation-tuples/check/openapi": {
        parameters: {
            query?: never
            header?: never
            path?: never
            cookie?: never
        }
        /**
         * Check a permission
         * @description To learn how relationship tuples and the check works, head over to [the documentation](https://www.ory.sh/docs/keto/concepts/api-overview).
         */
        get: operations["checkPermission"]
        put?: never
        /**
         * Check a permission
         * @description To learn how relationship tuples and the check works, head over to [the documentation](https://www.ory.sh/docs/keto/concepts/api-overview).
         */
        post: operations["postCheckPermission"]
        delete?: never
        options?: never
        head?: never
        patch?: never
        trace?: never
    }
    "/relation-tuples/expand": {
        parameters: {
            query?: never
            header?: never
            path?: never
            cookie?: never
        }
        /**
         * Expand a Relationship into permissions.
         * @description Use this endpoint to expand a relationship tuple into permissions.
         */
        get: operations["expandPermissions"]
        put?: never
        post?: never
        delete?: never
        options?: never
        head?: never
        patch?: never
        trace?: never
    }
    "/version": {
        parameters: {
            query?: never
            header?: never
            path?: never
            cookie?: never
        }
        /**
         * Return Running Software Version.
         * @description This endpoint returns the version of Ory Keto.
         *
         *     If the service supports TLS Edge Termination, this endpoint does not require the
         *     `X-Forwarded-Proto` header to be set.
         *
         *     Be aware that if you are running multiple nodes of this service, the version will never
         *     refer to the cluster state, only to a single instance.
         */
        get: operations["getVersion"]
        put?: never
        post?: never
        delete?: never
        options?: never
        head?: never
        patch?: never
        trace?: never
    }
}
export type webhooks = Record<string, never>
export interface components {
    schemas: {
        DefaultError: unknown
        ParseError: {
            end?: components["schemas"]["SourcePosition"]
            message?: string
            start?: components["schemas"]["SourcePosition"]
        }
        SourcePosition: {
            /** Format: int64 */
            Line?: number
            /** Format: int64 */
            column?: number
        }
        /** Format: uuid4 */
        UUID: string
        /** @description Ory Permission Language Document */
        checkOplSyntaxBody: string
        /** CheckOPLSyntaxResponse represents the response for an OPL syntax check request. */
        checkOplSyntaxResult: {
            /** @description The list of syntax errors */
            errors?: components["schemas"]["ParseError"][]
        }
        /**
         * Check Permission Result
         * @description The content of the allowed field is mirrored in the HTTP status code.
         */
        checkPermissionResult: {
            /** @description whether the relation tuple is allowed */
            allowed: boolean
        }
        /** @description Create Relationship Request Body */
        createRelationshipBody: {
            /** @description Namespace to query */
            namespace?: string
            /** @description Object to query */
            object?: string
            /** @description Relation to query */
            relation?: string
            /** @description SubjectID to query
             *
             *     Either SubjectSet or SubjectID can be provided. */
            subject_id?: string
            subject_set?: components["schemas"]["subjectSet"]
        }
        /**
         * JSON API Error Response
         * @description The standard Ory JSON API error format.
         */
        errorGeneric: {
            error: components["schemas"]["genericError"]
        }
        expandedPermissionTree: {
            /** @description The children of the node, possibly none. */
            children?: components["schemas"]["expandedPermissionTree"][]
            tuple?: components["schemas"]["relationship"]
            /**
             * @description The type of the node.
             *     union TreeNodeUnion
             *     exclusion TreeNodeExclusion
             *     intersection TreeNodeIntersection
             *     leaf TreeNodeLeaf
             *     tuple_to_subject_set TreeNodeTupleToSubjectSet
             *     computed_subject_set TreeNodeComputedSubjectSet
             *     not TreeNodeNot
             *     unspecified TreeNodeUnspecified
             * @enum {string}
             */
            type:
                | "union"
                | "exclusion"
                | "intersection"
                | "leaf"
                | "tuple_to_subject_set"
                | "computed_subject_set"
                | "not"
                | "unspecified"
        }
        genericError: {
            /**
             * Format: int64
             * @description The status code
             * @example 404
             */
            code?: number
            /**
             * @description Debug information
             *
             *     This field is often not exposed to protect against leaking
             *     sensitive information.
             * @example SQL field "foo" is not a bool.
             */
            debug?: string
            /** @description Further error details */
            details?: {
                [key: string]: unknown
            }
            /** @description The error ID
             *
             *     Useful when trying to identify various errors in application logic. */
            id?: string
            /**
             * @description Error message
             *
             *     The error's message.
             * @example The resource could not be found
             */
            message: string
            /**
             * @description A human-readable reason for the error
             * @example User with ID 1234 does not exist.
             */
            reason?: string
            /**
             * @description The request ID
             *
             *     The request ID is often exposed internally in order to trace
             *     errors across service architectures. This is often a UUID.
             * @example d7ef54b1-ec15-46e6-bccb-524b82c035e6
             */
            request?: string
            /**
             * @description The status description
             * @example Not Found
             */
            status?: string
        }
        healthNotReadyStatus: {
            /** @description Errors contains a list of errors that caused the not ready status. */
            errors?: {
                [key: string]: string
            }
        }
        healthStatus: {
            /** @description Status always contains "ok". */
            status?: string
        }
        namespace: {
            /** @description Name of the namespace. */
            name?: string
        }
        /** @description Check Permission using Post Request Body */
        postCheckPermissionBody: {
            /** @description Namespace to query */
            namespace?: string
            /** @description Object to query */
            object?: string
            /** @description Relation to query */
            relation?: string
            /** @description SubjectID to query
             *
             *     Either SubjectSet or SubjectID can be provided. */
            subject_id?: string
            subject_set?: components["schemas"]["subjectSet"]
        }
        /** @description Post Check Permission Or Error Body */
        postCheckPermissionOrErrorBody: {
            /** @description Namespace to query */
            namespace?: string
            /** @description Object to query */
            object?: string
            /** @description Relation to query */
            relation?: string
            /** @description SubjectID to query
             *
             *     Either SubjectSet or SubjectID can be provided. */
            subject_id?: string
            subject_set?: components["schemas"]["subjectSet"]
        }
        /** @description Relation Query */
        relationQuery: {
            /** @description Namespace to query */
            namespace?: string
            /** @description Object to query */
            object?: string
            /** @description Relation to query */
            relation?: string
            /** @description SubjectID to query
             *
             *     Either SubjectSet or SubjectID can be provided. */
            subject_id?: string
            subject_set?: components["schemas"]["subjectSet"]
        }
        /** @description Relationship */
        relationship: {
            /** @description Namespace of the Relation Tuple */
            namespace: string
            /** @description Object of the Relation Tuple */
            object: string
            /** @description Relation of the Relation Tuple */
            relation: string
            /** @description SubjectID of the Relation Tuple
             *
             *     Either SubjectSet or SubjectID can be provided. */
            subject_id?: string
            subject_set?: components["schemas"]["subjectSet"]
        }
        /** @description Relationship Namespace List */
        relationshipNamespaces: {
            namespaces?: components["schemas"]["namespace"][]
        }
        /** @description Payload for patching a relationship */
        relationshipPatch: {
            /** @enum {string} */
            action?: "insert" | "delete"
            relation_tuple?: components["schemas"]["relationship"]
        }
        /** @description Paginated Relationship List */
        relationships: {
            /** @description The opaque token to provide in a subsequent request
             *     to get the next page. It is the empty string iff this is
             *     the last page. */
            next_page_token?: string
            relation_tuples?: components["schemas"]["relationship"][]
        }
        subjectSet: {
            /** @description Namespace of the Subject Set */
            namespace: string
            /** @description Object of the Subject Set */
            object: string
            /** @description Relation of the Subject Set */
            relation: string
        }
        unexpectedError: string
        version: {
            /** @description Version is the service's version. */
            version?: string
        }
    }
    responses: {
        /** @description Empty responses are sent when, for example, resources are deleted. The HTTP status code for empty responses is typically 204. */
        emptyResponse: {
            headers: {
                [name: string]: unknown
            }
            content?: never
        }
    }
    parameters: never
    requestBodies: never
    headers: never
    pathItems: never
}
export type $defs = Record<string, never>
export interface operations {
    createRelationship: {
        parameters: {
            query?: never
            header?: never
            path?: never
            cookie?: never
        }
        requestBody?: {
            content: {
                "application/json": components["schemas"]["createRelationshipBody"]
            }
        }
        responses: {
            /** @description relationship */
            201: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["relationship"]
                }
            }
            /** @description errorGeneric */
            400: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
            /** @description errorGeneric */
            default: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
        }
    }
    deleteRelationships: {
        parameters: {
            query?: {
                /** @description Namespace of the Relationship */
                namespace?: string
                /** @description Object of the Relationship */
                object?: string
                /** @description Relation of the Relationship */
                relation?: string
                /** @description SubjectID of the Relationship */
                subject_id?: string
                /** @description Namespace of the Subject Set */
                "subject_set.namespace"?: string
                /** @description Object of the Subject Set */
                "subject_set.object"?: string
                /** @description Relation of the Subject Set */
                "subject_set.relation"?: string
            }
            header?: never
            path?: never
            cookie?: never
        }
        requestBody?: never
        responses: {
            204: components["responses"]["emptyResponse"]
            /** @description errorGeneric */
            400: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
            /** @description errorGeneric */
            default: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
        }
    }
    patchRelationships: {
        parameters: {
            query?: never
            header?: never
            path?: never
            cookie?: never
        }
        requestBody?: {
            content: {
                "application/json": components["schemas"]["relationshipPatch"][]
            }
        }
        responses: {
            204: components["responses"]["emptyResponse"]
            /** @description errorGeneric */
            400: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
            /** @description errorGeneric */
            404: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
            /** @description errorGeneric */
            default: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
        }
    }
    isAlive: {
        parameters: {
            query?: never
            header?: never
            path?: never
            cookie?: never
        }
        requestBody?: never
        responses: {
            /** @description Ory Keto is ready to accept connections. */
            200: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": {
                        /** @description Always "ok". */
                        status: string
                    }
                }
            }
            /** @description Unexpected error */
            default: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "text/plain": string
                }
            }
        }
    }
    isReady: {
        parameters: {
            query?: never
            header?: never
            path?: never
            cookie?: never
        }
        requestBody?: never
        responses: {
            /** @description Ory Keto is ready to accept requests. */
            200: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": {
                        /** @description Always "ok". */
                        status: string
                    }
                }
            }
            /** @description Ory Kratos is not yet ready to accept requests. */
            503: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": {
                        /** @description Errors contains a list of errors that caused the not ready status. */
                        errors: {
                            [key: string]: string
                        }
                    }
                }
            }
            /** @description Unexpected error */
            default: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "text/plain": string
                }
            }
        }
    }
    listRelationshipNamespaces: {
        parameters: {
            query?: never
            header?: never
            path?: never
            cookie?: never
        }
        requestBody?: never
        responses: {
            /** @description relationshipNamespaces */
            200: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["relationshipNamespaces"]
                }
            }
            /** @description errorGeneric */
            default: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
        }
    }
    checkOplSyntax: {
        parameters: {
            query?: never
            header?: never
            path?: never
            cookie?: never
        }
        requestBody?: {
            content: {
                "text/plain": components["schemas"]["checkOplSyntaxBody"]
            }
        }
        responses: {
            /** @description checkOplSyntaxResult */
            200: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["checkOplSyntaxResult"]
                }
            }
            /** @description errorGeneric */
            400: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
            /** @description errorGeneric */
            default: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
        }
    }
    getRelationships: {
        parameters: {
            query?: {
                page_token?: string
                page_size?: number
                /** @description Namespace of the Relationship */
                namespace?: string
                /** @description Object of the Relationship */
                object?: string
                /** @description Relation of the Relationship */
                relation?: string
                /** @description SubjectID of the Relationship */
                subject_id?: string
                /** @description Namespace of the Subject Set */
                "subject_set.namespace"?: string
                /** @description Object of the Subject Set */
                "subject_set.object"?: string
                /** @description Relation of the Subject Set */
                "subject_set.relation"?: string
            }
            header?: never
            path?: never
            cookie?: never
        }
        requestBody?: never
        responses: {
            /** @description relationships */
            200: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["relationships"]
                }
            }
            /** @description errorGeneric */
            404: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
            /** @description errorGeneric */
            default: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
        }
    }
    checkPermissionOrError: {
        parameters: {
            query?: {
                /** @description Namespace of the Relationship */
                namespace?: string
                /** @description Object of the Relationship */
                object?: string
                /** @description Relation of the Relationship */
                relation?: string
                /** @description SubjectID of the Relationship */
                subject_id?: string
                /** @description Namespace of the Subject Set */
                "subject_set.namespace"?: string
                /** @description Object of the Subject Set */
                "subject_set.object"?: string
                /** @description Relation of the Subject Set */
                "subject_set.relation"?: string
                "max-depth"?: number
            }
            header?: never
            path?: never
            cookie?: never
        }
        requestBody?: never
        responses: {
            /** @description checkPermissionResult */
            200: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["checkPermissionResult"]
                }
            }
            /** @description errorGeneric */
            400: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
            /** @description checkPermissionResult */
            403: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["checkPermissionResult"]
                }
            }
            /** @description errorGeneric */
            default: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
        }
    }
    postCheckPermissionOrError: {
        parameters: {
            query?: {
                "max-depth"?: number
            }
            header?: never
            path?: never
            cookie?: never
        }
        requestBody?: {
            content: {
                "application/json": components["schemas"]["postCheckPermissionOrErrorBody"]
            }
        }
        responses: {
            /** @description checkPermissionResult */
            200: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["checkPermissionResult"]
                }
            }
            /** @description errorGeneric */
            400: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
            /** @description checkPermissionResult */
            403: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["checkPermissionResult"]
                }
            }
            /** @description errorGeneric */
            default: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
        }
    }
    checkPermission: {
        parameters: {
            query?: {
                /** @description Namespace of the Relationship */
                namespace?: string
                /** @description Object of the Relationship */
                object?: string
                /** @description Relation of the Relationship */
                relation?: string
                /** @description SubjectID of the Relationship */
                subject_id?: string
                /** @description Namespace of the Subject Set */
                "subject_set.namespace"?: string
                /** @description Object of the Subject Set */
                "subject_set.object"?: string
                /** @description Relation of the Subject Set */
                "subject_set.relation"?: string
                "max-depth"?: number
            }
            header?: never
            path?: never
            cookie?: never
        }
        requestBody?: never
        responses: {
            /** @description checkPermissionResult */
            200: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["checkPermissionResult"]
                }
            }
            /** @description errorGeneric */
            400: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
            /** @description errorGeneric */
            default: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
        }
    }
    postCheckPermission: {
        parameters: {
            query?: {
                "max-depth"?: number
            }
            header?: never
            path?: never
            cookie?: never
        }
        requestBody?: {
            content: {
                "application/json": components["schemas"]["postCheckPermissionBody"]
            }
        }
        responses: {
            /** @description checkPermissionResult */
            200: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["checkPermissionResult"]
                }
            }
            /** @description errorGeneric */
            400: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
            /** @description errorGeneric */
            default: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
        }
    }
    expandPermissions: {
        parameters: {
            query: {
                /** @description Namespace of the Subject Set */
                namespace: string
                /** @description Object of the Subject Set */
                object: string
                /** @description Relation of the Subject Set */
                relation: string
                "max-depth"?: number
            }
            header?: never
            path?: never
            cookie?: never
        }
        requestBody?: never
        responses: {
            /** @description expandedPermissionTree */
            200: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["expandedPermissionTree"]
                }
            }
            /** @description errorGeneric */
            400: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
            /** @description errorGeneric */
            404: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
            /** @description errorGeneric */
            default: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": components["schemas"]["errorGeneric"]
                }
            }
        }
    }
    getVersion: {
        parameters: {
            query?: never
            header?: never
            path?: never
            cookie?: never
        }
        requestBody?: never
        responses: {
            /** @description Returns the Ory Keto version. */
            200: {
                headers: {
                    [name: string]: unknown
                }
                content: {
                    "application/json": {
                        /** @description The version of Ory Keto. */
                        version: string
                    }
                }
            }
        }
    }
}
