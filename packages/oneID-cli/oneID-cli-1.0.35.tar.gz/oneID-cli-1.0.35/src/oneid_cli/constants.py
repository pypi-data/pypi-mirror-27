# Copyright 2017 Neustar, Inc.  All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# has been included with this distribution in the LICENSE file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.


class TDIKeyStructureFlags(object):
    ROLE_UNDEF = 0x0000,
    ROLE_EXTERN = 0x0001     # /** General use for non-standard keys */,
    ROLE_F_S = 0x0002        # /** Fleet key. */,
    ROLE_F_C = 0x0003        # /** Fleet co-signer key. */,
    ROLE_DEVICE = 0x0004     # /** A device's SELF key. As represented to non-self actors. */,
    ROLE_SERVER = 0x0005     # /** A server's SELF key. As represented to non-self actors. */,
    ROLE_COSERV = 0x0006     # /** A cosigner's SELF key. As represented to non-self actors. */,
    ROLE_MASK = 0x0007       # /** This region of flag space overlaps with KeyRoles. */,
    EXPIRABLE = 0x0008       # /** This key may expire at some point. */,
    REVOKABLE = 0x0010       # /** This key can be revoked. */,
    INVALID = 0x0020         # /** This key is no longer valid. */,
    NET_ACCEPT = 0x0040      # /** Is acceptable for the network layer. */,
    APP_ACCEPT = 0x0080      # /** Is acceptable for the application layer. */,
    CAN_SIGN = 0x0100        # /** Is acceptable for the network layer. */,
    OUR_OWN = 0x0200         # /** This is our own identity. */,
    ORIGIN_PERSIST = 0x0400  # /** Key came from persistant storage (May be RW). */,
    ORIGIN_FLASH = 0x0800    # /** Key is baked into the executable. */,
    ORIGIN_GEN = 0x1000      # /** Was generated on this system. */,
    ORIGIN_EXTERN = 0x2000   # /** Came from outside. Usually from TLS. */,
    ORIGIN_HSM = 0x4000      # /** Came from an HSM or secure element. */,
    ORIGIN_PKI = 0x8000      # /** Imparted by a PKI. */,

    # /** These are the key origin flags. */
    ORIGIN_MASK = ORIGIN_PERSIST | ORIGIN_FLASH | ORIGIN_GEN | ORIGIN_EXTERN | ORIGIN_HSM | ORIGIN_PKI

    # /** These flags are meaningless to another system. */
    EXPORT_MASK = ~(CAN_SIGN | ORIGIN_GEN | ORIGIN_PERSIST | OUR_OWN)
