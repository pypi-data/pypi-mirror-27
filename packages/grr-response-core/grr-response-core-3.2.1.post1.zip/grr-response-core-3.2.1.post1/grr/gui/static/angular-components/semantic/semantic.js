'use strict';

// TODO(user): Auto-generate parts of this file
//
goog.provide('grrUi.semantic.module');

goog.require('grrUi.core.module');
goog.require('grrUi.core.semanticRegistry.SemanticRegistryService');

goog.require('grrUi.routing.module');

goog.require('grrUi.semantic.apiHuntResultDirective.ApiHuntResultDirective');
goog.require('grrUi.semantic.byteSizeDirective.ByteSizeDirective');
goog.require('grrUi.semantic.bytesDirective.BytesDirective');
goog.require('grrUi.semantic.clientUrnDirective.ClientUrnDirective');
goog.require('grrUi.semantic.dataObjectDirective.DataObjectDirective');
goog.require('grrUi.semantic.dictDirective.DictDirective');
goog.require('grrUi.semantic.durationDirective.DurationDirective');
goog.require('grrUi.semantic.encryptionKeyDirective.EncryptionKeyDirective');
goog.require('grrUi.semantic.flowIdDirective.FlowIdDirective');
goog.require('grrUi.semantic.hashDigestDirective.HashDigestDirective');
goog.require('grrUi.semantic.hashListDirective.HashListDirective');
goog.require('grrUi.semantic.huntIdDirective.HuntIdDirective');
goog.require('grrUi.semantic.jsonDirective.JsonDirective');
goog.require('grrUi.semantic.macAddressDirective.MacAddressDirective');
goog.require('grrUi.semantic.networkAddressDirective.NetworkAddressDirective');
goog.require('grrUi.semantic.objectLabelDirective.ObjectLabelDirective');
goog.require('grrUi.semantic.objectLabelsListDirective.ObjectLabelsListDirective');
goog.require('grrUi.semantic.primitiveDirective.PrimitiveDirective');
goog.require('grrUi.semantic.pseudo.module');

goog.require('grrUi.semantic.rekall.module');
goog.require('grrUi.semantic.rekallResponseDirective.RekallResponseDirective');

goog.require('grrUi.semantic.semanticDiffAnnotatedProtoDirective.SemanticDiffAnnotatedProtoDirective');
goog.require('grrUi.semantic.semanticProtoDirective.SemanticProtoDirective');
goog.require('grrUi.semantic.semanticProtosDiffDirective.SemanticProtosDiffDirective');
goog.require('grrUi.semantic.semanticValueDirective.RegistryOverrideDirective');
goog.require('grrUi.semantic.semanticValueDirective.SemanticValueDirective');
goog.require('grrUi.semantic.semanticVersionedProtoDirective.SemanticVersionedProtoDirective');
goog.require('grrUi.semantic.statEntryDirective.StatEntryDirective');
goog.require('grrUi.semantic.statModeDirective.StatModeDirective');
goog.require('grrUi.semantic.timestampDirective.TimestampDirective');
goog.require('grrUi.semantic.timestampSecondsDirective.TimestampSecondsDirective');
goog.require('grrUi.semantic.urnDirective.UrnDirective');


/**
 * Module with directives that render semantic values (i.e. RDFValues) fetched
 * from the server.
 */
grrUi.semantic.module = angular.module('grrUi.semantic',
                                       [grrUi.core.module.name,
                                        grrUi.routing.module.name,
                                        grrUi.semantic.pseudo.module.name,
                                        grrUi.semantic.rekall.module.name,
                                        'ui.bootstrap']);

grrUi.semantic.module.directive(
    grrUi.semantic.apiHuntResultDirective.ApiHuntResultDirective.directive_name,
    grrUi.semantic.apiHuntResultDirective.ApiHuntResultDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.byteSizeDirective.ByteSizeDirective.directive_name,
    grrUi.semantic.byteSizeDirective.ByteSizeDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.bytesDirective.BytesDirective.directive_name,
    grrUi.semantic.bytesDirective.BytesDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.clientUrnDirective.ClientUrnDirective.directive_name,
    grrUi.semantic.clientUrnDirective.ClientUrnDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.dataObjectDirective.DataObjectDirective.directive_name,
    grrUi.semantic.dataObjectDirective.DataObjectDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.dictDirective.DictDirective.directive_name,
    grrUi.semantic.dictDirective.DictDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.durationDirective.DurationDirective.directive_name,
    grrUi.semantic.durationDirective.DurationDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.encryptionKeyDirective.EncryptionKeyDirective.directive_name,
    grrUi.semantic.encryptionKeyDirective.EncryptionKeyDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.flowIdDirective.FlowIdDirective.directive_name,
    grrUi.semantic.flowIdDirective.FlowIdDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.hashDigestDirective.HashDigestDirective.directive_name,
    grrUi.semantic.hashDigestDirective.HashDigestDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.hashListDirective.HashListDirective.directive_name,
    grrUi.semantic.hashListDirective.HashListDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.huntIdDirective.HuntIdDirective.directive_name,
    grrUi.semantic.huntIdDirective.HuntIdDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.jsonDirective.JsonDirective.directive_name,
    grrUi.semantic.jsonDirective.JsonDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.macAddressDirective.MacAddressDirective.directive_name,
    grrUi.semantic.macAddressDirective.MacAddressDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.networkAddressDirective.
        NetworkAddressDirective.directive_name,
    grrUi.semantic.networkAddressDirective.NetworkAddressDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.objectLabelDirective.ObjectLabelDirective.directive_name,
    grrUi.semantic.objectLabelDirective.ObjectLabelDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.objectLabelsListDirective.ObjectLabelsListDirective
        .directive_name,
    grrUi.semantic.objectLabelsListDirective.ObjectLabelsListDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.primitiveDirective.PrimitiveDirective.directive_name,
    grrUi.semantic.primitiveDirective.PrimitiveDirective);

grrUi.semantic.module.directive(
    grrUi.semantic.rekallResponseDirective.RekallResponseDirective.directive_name,
    grrUi.semantic.rekallResponseDirective.RekallResponseDirective);

grrUi.semantic.module.directive(
    grrUi.semantic.semanticDiffAnnotatedProtoDirective
      .SemanticDiffAnnotatedProtoDirective.directive_name,
    grrUi.semantic.semanticDiffAnnotatedProtoDirective
      .SemanticDiffAnnotatedProtoDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.semanticProtoDirective.SemanticProtoDirective.directive_name,
    grrUi.semantic.semanticProtoDirective.SemanticProtoDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.semanticValueDirective.RegistryOverrideDirective.directive_name,
    grrUi.semantic.semanticValueDirective.RegistryOverrideDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.semanticValueDirective.SemanticValueDirective.directive_name,
    grrUi.semantic.semanticValueDirective.SemanticValueDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.semanticProtosDiffDirective.SemanticProtosDiffDirective
      .directive_name,
    grrUi.semantic.semanticProtosDiffDirective.SemanticProtosDiffDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.semanticVersionedProtoDirective
        .SemanticVersionedProtoDirective.directive_name,
    grrUi.semantic.semanticVersionedProtoDirective
        .SemanticVersionedProtoDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.statEntryDirective.StatEntryDirective.directive_name,
    grrUi.semantic.statEntryDirective.StatEntryDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.statModeDirective.StatModeDirective.directive_name,
    grrUi.semantic.statModeDirective.StatModeDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.timestampDirective.TimestampDirective.directive_name,
    grrUi.semantic.timestampDirective.TimestampDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.timestampSecondsDirective.TimestampSecondsDirective.directive_name,
    grrUi.semantic.timestampSecondsDirective.TimestampSecondsDirective);
grrUi.semantic.module.directive(
    grrUi.semantic.urnDirective.UrnDirective.directive_name,
    grrUi.semantic.urnDirective.UrnDirective);

grrUi.semantic.module.service(
    grrUi.core.semanticRegistry.SemanticRegistryService.values_service_name,
    grrUi.core.semanticRegistry.SemanticRegistryService);


grrUi.semantic.module.run(function(grrSemanticValueDirectivesRegistryService) {
  var registry = grrSemanticValueDirectivesRegistryService;

  registry.registerDirective(
      grrUi.semantic.apiHuntResultDirective.ApiHuntResultDirective.semantic_type,
      grrUi.semantic.apiHuntResultDirective.ApiHuntResultDirective);
  registry.registerDirective(
      grrUi.semantic.byteSizeDirective.ByteSizeDirective.semantic_type,
      grrUi.semantic.byteSizeDirective.ByteSizeDirective);
  angular.forEach(
      grrUi.semantic.bytesDirective.BytesDirective.semantic_types,
      function(type) {
        registry.registerDirective(type,
                                   grrUi.semantic.bytesDirective.BytesDirective);
      }.bind(this));
  angular.forEach(
      grrUi.semantic.clientUrnDirective.ClientUrnDirective.semantic_types,
      function(type) {
        registry.registerDirective(type,
                                   grrUi.semantic.clientUrnDirective.ClientUrnDirective);
      }.bind(this));
  registry.registerDirective(
      grrUi.semantic.dataObjectDirective.DataObjectDirective.semantic_type,
      grrUi.semantic.dataObjectDirective.DataObjectDirective);
  angular.forEach(
      grrUi.semantic.dictDirective.DictDirective.semantic_types,
      function(type) {
        registry.registerDirective(type,
                                   grrUi.semantic.dictDirective.DictDirective);
      }.bind(this));
  registry.registerDirective(
      grrUi.semantic.durationDirective.DurationDirective.semantic_type,
      grrUi.semantic.durationDirective.DurationDirective);
  registry.registerDirective(
      grrUi.semantic.encryptionKeyDirective.EncryptionKeyDirective
          .semantic_type,
      grrUi.semantic.encryptionKeyDirective.EncryptionKeyDirective);
  registry.registerDirective(
      grrUi.semantic.flowIdDirective.FlowIdDirective.semantic_type,
      grrUi.semantic.flowIdDirective.FlowIdDirective);
  registry.registerDirective(
      grrUi.semantic.hashDigestDirective.HashDigestDirective.semantic_type,
      grrUi.semantic.hashDigestDirective.HashDigestDirective);
  registry.registerDirective(
      grrUi.semantic.hashListDirective.HashListDirective.semantic_type,
      grrUi.semantic.hashListDirective.HashListDirective);
  registry.registerDirective(
      grrUi.semantic.huntIdDirective.HuntIdDirective.semantic_type,
      grrUi.semantic.huntIdDirective.HuntIdDirective);
  registry.registerDirective(
      grrUi.semantic.jsonDirective.JsonDirective.semantic_type,
      grrUi.semantic.jsonDirective.JsonDirective);
  registry.registerDirective(
      grrUi.semantic.macAddressDirective.MacAddressDirective.semantic_type,
      grrUi.semantic.macAddressDirective.MacAddressDirective);
  registry.registerDirective(
    grrUi.semantic.networkAddressDirective.NetworkAddressDirective
        .semantic_type,
    grrUi.semantic.networkAddressDirective.NetworkAddressDirective);
  registry.registerDirective(
    grrUi.semantic.objectLabelDirective.ObjectLabelDirective.semantic_type,
    grrUi.semantic.objectLabelDirective.ObjectLabelDirective);
  registry.registerDirective(
    grrUi.semantic.objectLabelDirective.ObjectLabelDirective.semantic_type,
    grrUi.semantic.objectLabelDirective.ObjectLabelDirective);
  registry.registerDirective(
    grrUi.semantic.objectLabelsListDirective.ObjectLabelsListDirective
        .semantic_type,
    grrUi.semantic.objectLabelsListDirective.ObjectLabelsListDirective);
  angular.forEach(
      grrUi.semantic.primitiveDirective.PrimitiveDirective.semantic_types,
      function(type) {
        registry.registerDirective(
            type, grrUi.semantic.primitiveDirective.PrimitiveDirective);
      }.bind(this));
  registry.registerDirective(
    grrUi.semantic.rekallResponseDirective.RekallResponseDirective.semantic_type,
    grrUi.semantic.rekallResponseDirective.RekallResponseDirective);
  registry.registerDirective(
    grrUi.semantic.semanticProtoDirective.SemanticProtoDirective.semantic_type,
    grrUi.semantic.semanticProtoDirective.SemanticProtoDirective);
  angular.forEach(
      grrUi.semantic.statEntryDirective.StatEntryDirective.semantic_types,
      function(type) {
        registry.registerDirective(type,
            grrUi.semantic.statEntryDirective.StatEntryDirective);
      }.bind(this));
  registry.registerDirective(
    grrUi.semantic.statModeDirective.StatModeDirective.semantic_type,
    grrUi.semantic.statModeDirective.StatModeDirective);
  registry.registerDirective(
    grrUi.semantic.timestampDirective.TimestampDirective.semantic_type,
    grrUi.semantic.timestampDirective.TimestampDirective);
  registry.registerDirective(
    grrUi.semantic.timestampSecondsDirective.TimestampSecondsDirective.semantic_type,
    grrUi.semantic.timestampSecondsDirective.TimestampSecondsDirective);
  registry.registerDirective(
    grrUi.semantic.urnDirective.UrnDirective.semantic_type,
    grrUi.semantic.urnDirective.UrnDirective);
});
