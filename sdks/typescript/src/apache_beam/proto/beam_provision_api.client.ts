// @generated by protobuf-ts 2.1.0 with parameter server_grpc1,generate_dependencies
// @generated from protobuf file "beam_provision_api.proto" (package "org.apache.beam.model.fn_execution.v1", syntax proto3)
// tslint:disable
//
//
// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
//
//
// Protocol Buffers describing the Provision API, for communicating with a runner
// for job and environment provisioning information over GRPC.
//
import type { RpcTransport } from "@protobuf-ts/runtime-rpc";
import type { ServiceInfo } from "@protobuf-ts/runtime-rpc";
import { ProvisionService } from "./beam_provision_api";
import { stackIntercept } from "@protobuf-ts/runtime-rpc";
import type { GetProvisionInfoResponse } from "./beam_provision_api";
import type { GetProvisionInfoRequest } from "./beam_provision_api";
import type { UnaryCall } from "@protobuf-ts/runtime-rpc";
import type { RpcOptions } from "@protobuf-ts/runtime-rpc";
/**
 * A service to provide runtime provisioning information to the SDK harness
 * worker instances -- such as pipeline options, resource constraints and
 * other job metadata -- needed by an SDK harness instance to initialize.
 *
 * @generated from protobuf service org.apache.beam.model.fn_execution.v1.ProvisionService
 */
export interface IProvisionServiceClient {
    /**
     * Get provision information for the SDK harness worker instance.
     *
     * @generated from protobuf rpc: GetProvisionInfo(org.apache.beam.model.fn_execution.v1.GetProvisionInfoRequest) returns (org.apache.beam.model.fn_execution.v1.GetProvisionInfoResponse);
     */
    getProvisionInfo(input: GetProvisionInfoRequest, options?: RpcOptions): UnaryCall<GetProvisionInfoRequest, GetProvisionInfoResponse>;
}
/**
 * A service to provide runtime provisioning information to the SDK harness
 * worker instances -- such as pipeline options, resource constraints and
 * other job metadata -- needed by an SDK harness instance to initialize.
 *
 * @generated from protobuf service org.apache.beam.model.fn_execution.v1.ProvisionService
 */
export class ProvisionServiceClient implements IProvisionServiceClient, ServiceInfo {
    typeName = ProvisionService.typeName;
    methods = ProvisionService.methods;
    options = ProvisionService.options;
    constructor(private readonly _transport: RpcTransport) {
    }
    /**
     * Get provision information for the SDK harness worker instance.
     *
     * @generated from protobuf rpc: GetProvisionInfo(org.apache.beam.model.fn_execution.v1.GetProvisionInfoRequest) returns (org.apache.beam.model.fn_execution.v1.GetProvisionInfoResponse);
     */
    getProvisionInfo(input: GetProvisionInfoRequest, options?: RpcOptions): UnaryCall<GetProvisionInfoRequest, GetProvisionInfoResponse> {
        const method = this.methods[0], opt = this._transport.mergeOptions(options);
        return stackIntercept<GetProvisionInfoRequest, GetProvisionInfoResponse>("unary", this._transport, method, opt, input);
    }
}
