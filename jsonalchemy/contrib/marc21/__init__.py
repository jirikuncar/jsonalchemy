from jsonalchemy import dsl
from jsonalchemy import utils


class Record(dsl.Model):

    control_number = dsl.Field()

    @control_number.creator('marc', '001')
    def control_number(self, value):
        return value

    control_number_identifier = dsl.Field()

    @control_number_identifier.creator('marc', '003')
    def control_number_identifier(self, value):
        return value

    date_and_time_of_latest_transaction = dsl.Field()

    @date_and_time_of_latest_transaction.creator('marc', '005')
    def date_and_time_of_latest_transaction(self, value):
        return value

    fixed_length_data_elements_additional_material_characteristics = dsl.Field()

    @fixed_length_data_elements_additional_material_characteristics.creator(
        'marc',
        '006')
    def fixed_length_data_elements_additional_material_characteristics(
            self,
            value):
        return value

    fixed_length_data_elements = dsl.Field()

    @fixed_length_data_elements.creator('marc', '008')
    def fixed_length_data_elements(self, value):
        return value

    library_of_congress_control_number = dsl.Object(
        lc_control_number=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        nucmc_control_number=dsl.Field(),
        canceled_invalid_lc_control_number=dsl.Field(),
    )

    @library_of_congress_control_number.creator('marc', '010..')
    @utils.filter_values
    def library_of_congress_control_number(self, value):
        return {
            'lc_control_number': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'nucmc_control_number': value.get('b'),
            'canceled_invalid_lc_control_number': value.get('z')}

    patent_control_information = dsl.List(dsl.Object(
        number=dsl.Field(),
        type_of_number=dsl.Field(),
        country=dsl.Field(),
        status=dsl.Field(),
        date=dsl.Field(),
        party_to_document=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @patent_control_information.creator('marc', '013..')
    @utils.for_each_value
    @utils.filter_values
    def patent_control_information(self, value):
        return {
            'number': value.get('a'),
            'type_of_number': value.get('c'),
            'country': value.get('b'),
            'status': value.get('e'),
            'date': value.get('d'),
            'party_to_document': value.get('f'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    national_bibliography_number = dsl.List(dsl.Object(
        national_bibliography_number=dsl.Field(),
        qualifying_information=dsl.Field(),
        source=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        canceled_invalid_national_bibliography_number=dsl.Field(),
    ))

    @national_bibliography_number.creator('marc', '015..')
    @utils.for_each_value
    @utils.filter_values
    def national_bibliography_number(self, value):
        return {
            'national_bibliography_number': value.get('a'),
            'qualifying_information': value.get('q'),
            'source': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'canceled_invalid_national_bibliography_number': value.get('z')}

    national_bibliographic_agency_control_number = dsl.List(dsl.Object(
        record_control_number=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        source=dsl.Field(),
        canceled_invalid_control_number=dsl.Field(),
    ))

    @national_bibliographic_agency_control_number.creator('marc', '016..')
    @utils.for_each_value
    @utils.filter_values
    def national_bibliographic_agency_control_number(self, value):
        return {
            'record_control_number': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'source': value.get('2'),
            'canceled_invalid_control_number': value.get('z')}

    copyright_or_legal_deposit_number = dsl.List(dsl.Object(
        copyright_or_legal_deposit_number=dsl.Field(),
        assigning_agency=dsl.Field(),
        date=dsl.Field(),
        display_text=dsl.Field(),
        source=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        canceled_invalid_copyright_or_legal_deposit_number=dsl.Field(),
    ))

    @copyright_or_legal_deposit_number.creator('marc', '017..')
    @utils.for_each_value
    @utils.filter_values
    def copyright_or_legal_deposit_number(self, value):
        return {
            'copyright_or_legal_deposit_number': value.get('a'),
            'assigning_agency': value.get('b'),
            'date': value.get('d'),
            'display_text': value.get('i'),
            'source': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'canceled_invalid_copyright_or_legal_deposit_number': value.get('z')}

    copyright_article_fee_code = dsl.Object(
        copyright_article_fee_code_nr=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        linkage=dsl.Field(),
    )

    @copyright_article_fee_code.creator('marc', '018..')
    @utils.filter_values
    def copyright_article_fee_code(self, value):
        return {
            'copyright_article_fee_code_nr': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'linkage': value.get('6')}

    international_standard_book_number = dsl.List(dsl.Object(
        international_standard_book_number=dsl.Field(),
        terms_of_availability=dsl.Field(),
        qualifying_information=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        canceled_invalid_isbn=dsl.Field(),
    ))

    @international_standard_book_number.creator('marc', '020..')
    @utils.for_each_value
    @utils.filter_values
    def international_standard_book_number(self, value):
        return {
            'international_standard_book_number': value.get('a'),
            'terms_of_availability': value.get('c'),
            'qualifying_information': value.get('q'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'canceled_invalid_isbn': value.get('z')}

    international_standard_serial_number = dsl.List(dsl.Object(
        international_standard_serial_number=dsl.Field(),
        canceled_issn_l=dsl.Field(),
        issn_l=dsl.Field(),
        source=dsl.Field(),
        linkage=dsl.Field(),
        incorrect_issn=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        canceled_issn=dsl.Field(),
    ))

    @international_standard_serial_number.creator('marc', '022..')
    @utils.for_each_value
    @utils.filter_values
    def international_standard_serial_number(self, value):
        return {
            'international_standard_serial_number': value.get('a'),
            'canceled_issn_l': value.get('m'),
            'issn_l': value.get('l'),
            'source': value.get('2'),
            'linkage': value.get('6'),
            'incorrect_issn': value.get('y'),
            'field_link_and_sequence_number': value.get('8'),
            'canceled_issn': value.get('z')}

    other_standard_identifier = dsl.List(dsl.Object(
        standard_number_or_code=dsl.Field(),
        terms_of_availability=dsl.Field(),
        additional_codes_following_the_standard_number_or_code=dsl.Field(),
        qualifying_information=dsl.Field(),
        source_of_number_or_code=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        canceled_invalid_standard_number_or_code=dsl.Field(),
    ))

    @other_standard_identifier.creator('marc', '024..')
    @utils.for_each_value
    @utils.filter_values
    def other_standard_identifier(self, value):
        return {
            'standard_number_or_code': value.get('a'),
            'terms_of_availability': value.get('c'),
            'additional_codes_following_the_standard_number_or_code': value.get('d'),
            'qualifying_information': value.get('q'),
            'source_of_number_or_code': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'canceled_invalid_standard_number_or_code': value.get('z')}

    overseas_acquisition_number = dsl.List(dsl.Object(
        overseas_acquisition_number=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @overseas_acquisition_number.creator('marc', '025..')
    @utils.for_each_value
    @utils.filter_values
    def overseas_acquisition_number(self, value):
        return {
            'overseas_acquisition_number': value.get('a'),
            'field_link_and_sequence_number': value.get('8')}

    fingerprint_identifier = dsl.List(dsl.Object(
        first_and_second_groups_of_characters=dsl.Field(),
        date=dsl.Field(),
        third_and_fourth_groups_of_characters=dsl.Field(),
        unparsed_fingerprint=dsl.Field(),
        number_of_volume_or_part=dsl.Field(),
        source=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @fingerprint_identifier.creator('marc', '026..')
    @utils.for_each_value
    @utils.filter_values
    def fingerprint_identifier(self, value):
        return {
            'first_and_second_groups_of_characters': value.get('a'),
            'date': value.get('c'),
            'third_and_fourth_groups_of_characters': value.get('b'),
            'unparsed_fingerprint': value.get('e'),
            'number_of_volume_or_part': value.get('d'),
            'source': value.get('2'),
            'institution_to_which_field_applies': value.get('5'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    standard_technical_report_number = dsl.List(dsl.Object(
        standard_technical_report_number=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        canceled_invalid_number=dsl.Field(),
        qualifying_information=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @standard_technical_report_number.creator('marc', '027..')
    @utils.for_each_value
    @utils.filter_values
    def standard_technical_report_number(self, value):
        return {
            'standard_technical_report_number': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'canceled_invalid_number': value.get('z'),
            'qualifying_information': value.get('q'),
            'linkage': value.get('6')}

    publisher_number = dsl.List(dsl.Object(
        publisher_number=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        source=dsl.Field(),
        qualifying_information=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @publisher_number.creator('marc', '028..')
    @utils.for_each_value
    @utils.filter_values
    def publisher_number(self, value):
        return {
            'publisher_number': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'source': value.get('b'),
            'qualifying_information': value.get('q'),
            'linkage': value.get('6')}

    coden_designation = dsl.List(dsl.Object(
        coden=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        canceled_invalid_coden=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @coden_designation.creator('marc', '030..')
    @utils.for_each_value
    @utils.filter_values
    def coden_designation(self, value):
        return {
            'coden': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'canceled_invalid_coden': value.get('z'),
            'linkage': value.get('6')}

    musical_incipits_information = dsl.List(dsl.Object(
        number_of_work=dsl.Field(),
        number_of_excerpt=dsl.Field(),
        number_of_movement=dsl.Field(),
        role=dsl.Field(),
        caption_or_heading=dsl.Field(),
        clef=dsl.Field(),
        public_note=dsl.Field(),
        voice_instrument=dsl.Field(),
        time_signature=dsl.Field(),
        key_signature=dsl.Field(),
        general_note=dsl.Field(),
        musical_notation=dsl.Field(),
        coded_validity_note=dsl.Field(),
        system_code=dsl.Field(),
        uniform_resource_identifier=dsl.Field(),
        text_incipit=dsl.Field(),
        linkage=dsl.Field(),
        link_text=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        key_or_mode=dsl.Field(),
    ))

    @musical_incipits_information.creator('marc', '031..')
    @utils.for_each_value
    @utils.filter_values
    def musical_incipits_information(self, value):
        return {
            'number_of_work': value.get('a'),
            'number_of_excerpt': value.get('c'),
            'number_of_movement': value.get('b'),
            'role': value.get('e'),
            'caption_or_heading': value.get('d'),
            'clef': value.get('g'),
            'public_note': value.get('z'),
            'voice_instrument': value.get('m'),
            'time_signature': value.get('o'),
            'key_signature': value.get('n'),
            'general_note': value.get('q'),
            'musical_notation': value.get('p'),
            'coded_validity_note': value.get('s'),
            'system_code': value.get('2'),
            'uniform_resource_identifier': value.get('u'),
            'text_incipit': value.get('t'),
            'linkage': value.get('6'),
            'link_text': value.get('y'),
            'field_link_and_sequence_number': value.get('8'),
            'key_or_mode': value.get('r')}

    postal_registration_number = dsl.List(dsl.Object(
        postal_registration_number=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        source_agency_assigning_number=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @postal_registration_number.creator('marc', '032..')
    @utils.for_each_value
    @utils.filter_values
    def postal_registration_number(self, value):
        return {
            'postal_registration_number': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'source_agency_assigning_number': value.get('b'),
            'linkage': value.get('6')}

    date_time_and_place_of_an_event = dsl.List(dsl.Object(
        formatted_date_time=dsl.Field(),
        geographic_classification_subarea_code=dsl.Field(),
        geographic_classification_area_code=dsl.Field(),
        place_of_event=dsl.Field(),
        authority_record_control_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source_of_term=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @date_time_and_place_of_an_event.creator('marc', '033..')
    @utils.for_each_value
    @utils.filter_values
    def date_time_and_place_of_an_event(self, value):
        return {
            'formatted_date_time': value.get('a'),
            'geographic_classification_subarea_code': value.get('c'),
            'geographic_classification_area_code': value.get('b'),
            'place_of_event': value.get('p'),
            'authority_record_control_number': value.get('0'),
            'materials_specified': value.get('3'),
            'source_of_term': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    coded_cartographic_mathematical_data = dsl.List(dsl.Object(
        authority_record_control_number_or_standard_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        category_of_scale=dsl.Field(),
        constant_ratio_linear_vertical_scale=dsl.Field(),
        constant_ratio_linear_horizontal_scale=dsl.Field(),
        coordinates_easternmost_longitude=dsl.Field(),
        coordinates_westernmost_longitude=dsl.Field(),
        coordinates_southernmost_latitude=dsl.Field(),
        coordinates_northernmost_latitude=dsl.Field(),
        angular_scale=dsl.Field(),
        declination_southern_limit=dsl.Field(),
        declination_northern_limit=dsl.Field(),
        right_ascension_eastern_limit=dsl.Field(),
        right_ascension_western_limit=dsl.Field(),
        equinox=dsl.Field(),
        g_ring_latitude=dsl.Field(),
        distance_from_earth=dsl.Field(),
        g_ring_longitude=dsl.Field(),
        ending_date=dsl.Field(),
        beginning_date=dsl.Field(),
        name_of_extraterrestrial_body=dsl.Field(),
    ))

    @coded_cartographic_mathematical_data.creator('marc', '034..')
    @utils.for_each_value
    @utils.filter_values
    def coded_cartographic_mathematical_data(self, value):
        return {
            'authority_record_control_number_or_standard_number': value.get('0'),
            'materials_specified': value.get('3'),
            'source': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'category_of_scale': value.get('a'),
            'constant_ratio_linear_vertical_scale': value.get('c'),
            'constant_ratio_linear_horizontal_scale': value.get('b'),
            'coordinates_easternmost_longitude': value.get('e'),
            'coordinates_westernmost_longitude': value.get('d'),
            'coordinates_southernmost_latitude': value.get('g'),
            'coordinates_northernmost_latitude': value.get('f'),
            'angular_scale': value.get('h'),
            'declination_southern_limit': value.get('k'),
            'declination_northern_limit': value.get('j'),
            'right_ascension_eastern_limit': value.get('m'),
            'right_ascension_western_limit': value.get('n'),
            'equinox': value.get('p'),
            'g_ring_latitude': value.get('s'),
            'distance_from_earth': value.get('r'),
            'g_ring_longitude': value.get('t'),
            'ending_date': value.get('y'),
            'beginning_date': value.get('x'),
            'name_of_extraterrestrial_body': value.get('z')}

    system_control_number = dsl.List(dsl.Object(
        system_control_number=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        canceled_invalid_control_number=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @system_control_number.creator('marc', '035..')
    @utils.for_each_value
    @utils.filter_values
    def system_control_number(self, value):
        return {
            'system_control_number': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'canceled_invalid_control_number': value.get('z'),
            'linkage': value.get('6')}

    original_study_number_for_computer_data_files = dsl.Object(
        original_study_number=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        source_agency_assigning_number=dsl.Field(),
        linkage=dsl.Field(),
    )

    @original_study_number_for_computer_data_files.creator('marc', '036..')
    @utils.filter_values
    def original_study_number_for_computer_data_files(self, value):
        return {
            'original_study_number': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'source_agency_assigning_number': value.get('b'),
            'linkage': value.get('6')}

    source_of_acquisition = dsl.List(dsl.Object(
        stock_number=dsl.Field(),
        terms_of_availability=dsl.Field(),
        source_of_stock_number_acquisition=dsl.Field(),
        additional_format_characteristics=dsl.Field(),
        form_of_issue=dsl.Field(),
        note=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @source_of_acquisition.creator('marc', '037..')
    @utils.for_each_value
    @utils.filter_values
    def source_of_acquisition(self, value):
        return {
            'stock_number': value.get('a'),
            'terms_of_availability': value.get('c'),
            'source_of_stock_number_acquisition': value.get('b'),
            'additional_format_characteristics': value.get('g'),
            'form_of_issue': value.get('f'),
            'note': value.get('n'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    record_content_licensor = dsl.Object(
        record_content_licensor=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        linkage=dsl.Field(),
    )

    @record_content_licensor.creator('marc', '038..')
    @utils.filter_values
    def record_content_licensor(self, value):
        return {
            'record_content_licensor': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'linkage': value.get('6')}

    cataloging_source = dsl.Object(
        original_cataloging_agency=dsl.Field(),
        transcribing_agency=dsl.Field(),
        language_of_cataloging=dsl.Field(),
        description_conventions=dsl.Field(),
        modifying_agency=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    )

    @cataloging_source.creator('marc', '040..')
    @utils.filter_values
    def cataloging_source(self, value):
        return {
            'original_cataloging_agency': value.get('a'),
            'transcribing_agency': value.get('c'),
            'language_of_cataloging': value.get('b'),
            'description_conventions': value.get('e'),
            'modifying_agency': value.get('d'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    language_code = dsl.List(
        dsl.Object(
            language_code_of_text_sound_track_or_separate_title=dsl.Field(),
            language_code_of_summary_or_abstract=dsl.Field(),
            language_code_of_librettos=dsl.Field(),
            language_code_of_sung_or_spoken_text=dsl.Field(),
            language_code_of_accompanying_material_other_than_librettos=dsl.Field(),
            language_code_of_table_of_contents=dsl.Field(),
            language_code_of_original=dsl.Field(),
            language_code_of_intermediate_translations=dsl.Field(),
            language_code_of_subtitles_or_captions=dsl.Field(),
            language_code_of_original_accompanying_materials_other_than_librettos=dsl.Field(),
            language_code_of_original_libretto=dsl.Field(),
            source_of_code=dsl.Field(),
            linkage=dsl.Field(),
            field_link_and_sequence_number=dsl.Field(),
        ))

    @language_code.creator('marc', '041..')
    @utils.for_each_value
    @utils.filter_values
    def language_code(self, value):
        return {
            'language_code_of_text_sound_track_or_separate_title': value.get('a'),
            'language_code_of_summary_or_abstract': value.get('b'),
            'language_code_of_librettos': value.get('e'),
            'language_code_of_sung_or_spoken_text': value.get('d'),
            'language_code_of_accompanying_material_other_than_librettos': value.get('g'),
            'language_code_of_table_of_contents': value.get('f'),
            'language_code_of_original': value.get('h'),
            'language_code_of_intermediate_translations': value.get('k'),
            'language_code_of_subtitles_or_captions': value.get('j'),
            'language_code_of_original_accompanying_materials_other_than_librettos': value.get('m'),
            'language_code_of_original_libretto': value.get('n'),
            'source_of_code': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    authentication_code = dsl.Object(
        authentication_code=dsl.Field(),
    )

    @authentication_code.creator('marc', '042..')
    @utils.filter_values
    def authentication_code(self, value):
        return {'authentication_code': value.get('a')}

    geographic_area_code = dsl.Object(
        geographic_area_code=dsl.Field(),
        iso_code=dsl.Field(),
        local_gac_code=dsl.Field(),
        authority_record_control_number_or_standard_number=dsl.Field(),
        source_of_local_code=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    )

    @geographic_area_code.creator('marc', '043..')
    @utils.filter_values
    def geographic_area_code(self, value):
        return {
            'geographic_area_code': value.get('a'),
            'iso_code': value.get('c'),
            'local_gac_code': value.get('b'),
            'authority_record_control_number_or_standard_number': value.get('0'),
            'source_of_local_code': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    country_of_publishing_producing_entity_code = dsl.Object(
        marc_country_code=dsl.Field(),
        iso_country_code=dsl.Field(),
        local_subentity_code=dsl.Field(),
        source_of_local_subentity_code=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    )

    @country_of_publishing_producing_entity_code.creator('marc', '044..')
    @utils.filter_values
    def country_of_publishing_producing_entity_code(self, value):
        return {
            'marc_country_code': value.get('a'),
            'iso_country_code': value.get('c'),
            'local_subentity_code': value.get('b'),
            'source_of_local_subentity_code': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    time_period_of_content = dsl.Object(
        time_period_code=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        formatted_pre_9999_bc_time_period=dsl.Field(),
        formatted_9999_bc_through_ce_time_period=dsl.Field(),
        linkage=dsl.Field(),
    )

    @time_period_of_content.creator('marc', '045..')
    @utils.filter_values
    def time_period_of_content(self, value):
        return {
            'time_period_code': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'formatted_pre_9999_bc_time_period': value.get('c'),
            'formatted_9999_bc_through_ce_time_period': value.get('b'),
            'linkage': value.get('6')}

    special_coded_dates = dsl.List(dsl.Object(
        type_of_date_code=dsl.Field(),
        date_1_ce_date=dsl.Field(),
        date_1_bc_date=dsl.Field(),
        date_2_ce_date=dsl.Field(),
        date_2_bc_date=dsl.Field(),
        beginning_or_single_date_created=dsl.Field(),
        date_resource_modified=dsl.Field(),
        beginning_of_date_valid=dsl.Field(),
        ending_date_created=dsl.Field(),
        single_or_starting_date_for_aggregated_content=dsl.Field(),
        end_of_date_valid=dsl.Field(),
        ending_date_for_aggregated_content=dsl.Field(),
        source_of_date=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @special_coded_dates.creator('marc', '046..')
    @utils.for_each_value
    @utils.filter_values
    def special_coded_dates(self, value):
        return {
            'type_of_date_code': value.get('a'),
            'date_1_ce_date': value.get('c'),
            'date_1_bc_date': value.get('b'),
            'date_2_ce_date': value.get('e'),
            'date_2_bc_date': value.get('d'),
            'beginning_or_single_date_created': value.get('k'),
            'date_resource_modified': value.get('j'),
            'beginning_of_date_valid': value.get('m'),
            'ending_date_created': value.get('l'),
            'single_or_starting_date_for_aggregated_content': value.get('o'),
            'end_of_date_valid': value.get('n'),
            'ending_date_for_aggregated_content': value.get('p'),
            'source_of_date': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    form_of_musical_composition_code = dsl.List(dsl.Object(
        form_of_musical_composition_code=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        source_of_code=dsl.Field(),
    ))

    @form_of_musical_composition_code.creator('marc', '047..')
    @utils.for_each_value
    @utils.filter_values
    def form_of_musical_composition_code(self, value):
        return {
            'form_of_musical_composition_code': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'source_of_code': value.get('2')}

    number_of_musical_instruments_or_voices_code = dsl.List(dsl.Object(
        performer_or_ensemble=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        source_of_code=dsl.Field(),
        soloist=dsl.Field(),
    ))

    @number_of_musical_instruments_or_voices_code.creator('marc', '048..')
    @utils.for_each_value
    @utils.filter_values
    def number_of_musical_instruments_or_voices_code(self, value):
        return {
            'performer_or_ensemble': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'source_of_code': value.get('2'),
            'soloist': value.get('b')}

    library_of_congress_call_number = dsl.List(dsl.Object(
        classification_number=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        materials_specified=dsl.Field(),
        item_number=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @library_of_congress_call_number.creator('marc', '050..')
    @utils.for_each_value
    @utils.filter_values
    def library_of_congress_call_number(self, value):
        return {
            'classification_number': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'materials_specified': value.get('3'),
            'item_number': value.get('b'),
            'linkage': value.get('6')}

    library_of_congress_copy_issue_offprint_statement = dsl.List(dsl.Object(
        classification_number=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        copy_information=dsl.Field(),
        item_number=dsl.Field(),
    ))

    @library_of_congress_copy_issue_offprint_statement.creator('marc', '051..')
    @utils.for_each_value
    @utils.filter_values
    def library_of_congress_copy_issue_offprint_statement(self, value):
        return {
            'classification_number': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'copy_information': value.get('c'),
            'item_number': value.get('b')}

    geographic_classification = dsl.List(dsl.Object(
        geographic_classification_area_code=dsl.Field(),
        geographic_classification_subarea_code=dsl.Field(),
        populated_place_name=dsl.Field(),
        code_source=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @geographic_classification.creator('marc', '052..')
    @utils.for_each_value
    @utils.filter_values
    def geographic_classification(self, value):
        return {
            'geographic_classification_area_code': value.get('a'),
            'geographic_classification_subarea_code': value.get('b'),
            'populated_place_name': value.get('d'),
            'code_source': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    classification_numbers_assigned_in_canada = dsl.List(dsl.Object(
        classification_number=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        source_of_call_class_number=dsl.Field(),
        item_number=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @classification_numbers_assigned_in_canada.creator('marc', '055..')
    @utils.for_each_value
    @utils.filter_values
    def classification_numbers_assigned_in_canada(self, value):
        return {
            'classification_number': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'source_of_call_class_number': value.get('2'),
            'item_number': value.get('b'),
            'linkage': value.get('6')}

    national_library_of_medicine_call_number = dsl.List(dsl.Object(
        classification_number_r=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        item_number=dsl.Field(),
    ))

    @national_library_of_medicine_call_number.creator('marc', '060..')
    @utils.for_each_value
    @utils.filter_values
    def national_library_of_medicine_call_number(self, value):
        return {
            'classification_number_r': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'item_number': value.get('b')}

    national_library_of_medicine_copy_statement = dsl.List(dsl.Object(
        classification_number=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        copy_information=dsl.Field(),
        item_number=dsl.Field(),
    ))

    @national_library_of_medicine_copy_statement.creator('marc', '061..')
    @utils.for_each_value
    @utils.filter_values
    def national_library_of_medicine_copy_statement(self, value):
        return {
            'classification_number': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'copy_information': value.get('c'),
            'item_number': value.get('b')}

    character_sets_present = dsl.Object(
        primary_g0_character_set=dsl.Field(),
        alternate_g0_or_g1_character_set=dsl.Field(),
        primary_g1_character_set=dsl.Field(),
    )

    @character_sets_present.creator('marc', '066..')
    @utils.filter_values
    def character_sets_present(self, value):
        return {
            'primary_g0_character_set': value.get('a'),
            'alternate_g0_or_g1_character_set': value.get('c'),
            'primary_g1_character_set': value.get('b')}

    national_agricultural_library_call_number = dsl.List(dsl.Object(
        classification_number=dsl.Field(),
        field_link_and_sequence_number_r=dsl.Field(),
        item_number=dsl.Field(),
    ))

    @national_agricultural_library_call_number.creator('marc', '070..')
    @utils.for_each_value
    @utils.filter_values
    def national_agricultural_library_call_number(self, value):
        return {
            'classification_number': value.get('a'),
            'field_link_and_sequence_number_r': value.get('8'),
            'item_number': value.get('b')}

    national_agricultural_library_copy_statement = dsl.List(dsl.Object(
        classification_number=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        copy_information=dsl.Field(),
        item_number=dsl.Field(),
    ))

    @national_agricultural_library_copy_statement.creator('marc', '071..')
    @utils.for_each_value
    @utils.filter_values
    def national_agricultural_library_copy_statement(self, value):
        return {
            'classification_number': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'copy_information': value.get('c'),
            'item_number': value.get('b')}

    subject_category_code = dsl.List(dsl.Object(
        subject_category_code=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        source=dsl.Field(),
        subject_category_code_subdivision=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @subject_category_code.creator('marc', '072..')
    @utils.for_each_value
    @utils.filter_values
    def subject_category_code(self, value):
        return {
            'subject_category_code': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'source': value.get('2'),
            'subject_category_code_subdivision': value.get('x'),
            'linkage': value.get('6')}

    gpo_item_number = dsl.List(dsl.Object(
        gpo_item_number=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        canceled_invalid_gpo_item_number=dsl.Field(),
    ))

    @gpo_item_number.creator('marc', '074..')
    @utils.for_each_value
    @utils.filter_values
    def gpo_item_number(self, value):
        return {
            'gpo_item_number': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'canceled_invalid_gpo_item_number': value.get('z')}

    universal_decimal_classification_number = dsl.List(dsl.Object(
        universal_decimal_classification_number=dsl.Field(),
        item_number=dsl.Field(),
        linkage=dsl.Field(),
        edition_identifier=dsl.Field(),
        common_auxiliary_subdivision=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @universal_decimal_classification_number.creator('marc', '080..')
    @utils.for_each_value
    @utils.filter_values
    def universal_decimal_classification_number(self, value):
        return {
            'universal_decimal_classification_number': value.get('a'),
            'item_number': value.get('b'),
            'linkage': value.get('6'),
            'edition_identifier': value.get('2'),
            'common_auxiliary_subdivision': value.get('x'),
            'field_link_and_sequence_number': value.get('8')}

    dewey_decimal_classification_number = dsl.List(dsl.Object(
        classification_number=dsl.Field(),
        item_number=dsl.Field(),
        standard_or_optional_designation=dsl.Field(),
        assigning_agency=dsl.Field(),
        edition_number=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @dewey_decimal_classification_number.creator('marc', '082..')
    @utils.for_each_value
    @utils.filter_values
    def dewey_decimal_classification_number(self, value):
        return {
            'classification_number': value.get('a'),
            'item_number': value.get('b'),
            'standard_or_optional_designation': value.get('m'),
            'assigning_agency': value.get('q'),
            'edition_number': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    additional_dewey_decimal_classification_number = dsl.List(
        dsl.Object(
            classification_number=dsl.Field(),
            classification_number_ending_number_of_span=dsl.Field(),
            standard_or_optional_designation=dsl.Field(),
            assigning_agency=dsl.Field(),
            edition_number=dsl.Field(),
            linkage=dsl.Field(),
            table_sequence_number_for_internal_subarrangement_or_add_table=dsl.Field(),
            field_link_and_sequence_number=dsl.Field(),
            table_identification=dsl.Field(),
        ))

    @additional_dewey_decimal_classification_number.creator('marc', '083..')
    @utils.for_each_value
    @utils.filter_values
    def additional_dewey_decimal_classification_number(self, value):
        return {
            'classification_number': value.get('a'),
            'classification_number_ending_number_of_span': value.get('c'),
            'standard_or_optional_designation': value.get('m'),
            'assigning_agency': value.get('q'),
            'edition_number': value.get('2'),
            'linkage': value.get('6'),
            'table_sequence_number_for_internal_subarrangement_or_add_table': value.get('y'),
            'field_link_and_sequence_number': value.get('8'),
            'table_identification': value.get('z')}

    other_classification_number = dsl.List(dsl.Object(
        classification_number=dsl.Field(),
        item_number=dsl.Field(),
        assigning_agency=dsl.Field(),
        number_source=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @other_classification_number.creator('marc', '084..')
    @utils.for_each_value
    @utils.filter_values
    def other_classification_number(self, value):
        return {
            'classification_number': value.get('a'),
            'item_number': value.get('b'),
            'assigning_agency': value.get('q'),
            'number_source': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    synthesized_classification_number_components = dsl.List(
        dsl.Object(
            number_where_instructions_are_found_single_number_or_beginning_number_of_span=dsl.Field(),
            classification_number_ending_number_of_span=dsl.Field(),
            base_number=dsl.Field(),
            facet_designator=dsl.Field(),
            number_in_internal_subarrangement_or_add_table_where_instructions_are_found=dsl.Field(),
            digits_added_from_classification_number_in_schedule_or_external_table=dsl.Field(),
            root_number=dsl.Field(),
            number_being_analyzed=dsl.Field(),
            digits_added_from_internal_subarrangement_or_add_table=dsl.Field(),
            table_identification_internal_subarrangement_or_add_table=dsl.Field(),
            linkage=dsl.Field(),
            table_sequence_number_for_internal_subarrangement_or_add_table=dsl.Field(),
            field_link_and_sequence_number=dsl.Field(),
            table_identification=dsl.Field(),
        ))

    @synthesized_classification_number_components.creator('marc', '085..')
    @utils.for_each_value
    @utils.filter_values
    def synthesized_classification_number_components(self, value):
        return {
            'number_where_instructions_are_found_single_number_or_beginning_number_of_span': value.get('a'),
            'classification_number_ending_number_of_span': value.get('c'),
            'base_number': value.get('b'),
            'facet_designator': value.get('f'),
            'number_in_internal_subarrangement_or_add_table_where_instructions_are_found': value.get('v'),
            'digits_added_from_classification_number_in_schedule_or_external_table': value.get('s'),
            'root_number': value.get('r'),
            'number_being_analyzed': value.get('u'),
            'digits_added_from_internal_subarrangement_or_add_table': value.get('t'),
            'table_identification_internal_subarrangement_or_add_table': value.get('w'),
            'linkage': value.get('6'),
            'table_sequence_number_for_internal_subarrangement_or_add_table': value.get('y'),
            'field_link_and_sequence_number': value.get('8'),
            'table_identification': value.get('z')}

    government_document_classification_number = dsl.List(dsl.Object(
        classification_number=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        number_source=dsl.Field(),
        canceled_invalid_classification_number=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @government_document_classification_number.creator('marc', '086..')
    @utils.for_each_value
    @utils.filter_values
    def government_document_classification_number(self, value):
        return {
            'classification_number': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'number_source': value.get('2'),
            'canceled_invalid_classification_number': value.get('z'),
            'linkage': value.get('6')}

    report_number = dsl.List(dsl.Object(
        report_number=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        canceled_invalid_report_number=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @report_number.creator('marc', '088..')
    @utils.for_each_value
    @utils.filter_values
    def report_number(self, value):
        return {
            'report_number': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'canceled_invalid_report_number': value.get('z'),
            'linkage': value.get('6')}

    main_entry_personal_name = dsl.Object(
        personal_name=dsl.Field(),
        titles_and_words_associated_with_a_name=dsl.Field(),
        numeration=dsl.Field(),
        relator_term=dsl.Field(),
        dates_associated_with_a_name=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_of_a_work=dsl.Field(),
        form_subheading=dsl.Field(),
        attribution_qualifier=dsl.Field(),
        language_of_a_work=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        number_of_part_section_of_a_work=dsl.Field(),
        fuller_form_of_name=dsl.Field(),
        authority_record_control_number=dsl.Field(),
        affiliation=dsl.Field(),
        relator_code=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        title_of_a_work=dsl.Field(),
    )

    @main_entry_personal_name.creator('marc', '100..')
    @utils.filter_values
    def main_entry_personal_name(self, value):
        return {
            'personal_name': value.get('a'),
            'titles_and_words_associated_with_a_name': value.get('c'),
            'numeration': value.get('b'),
            'relator_term': value.get('e'),
            'dates_associated_with_a_name': value.get('d'),
            'miscellaneous_information': value.get('g'),
            'date_of_a_work': value.get('f'),
            'form_subheading': value.get('k'),
            'attribution_qualifier': value.get('j'),
            'language_of_a_work': value.get('l'),
            'name_of_part_section_of_a_work': value.get('p'),
            'number_of_part_section_of_a_work': value.get('n'),
            'fuller_form_of_name': value.get('q'),
            'authority_record_control_number': value.get('0'),
            'affiliation': value.get('u'),
            'relator_code': value.get('4'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'title_of_a_work': value.get('t')}

    main_entry_corporate_name = dsl.Object(
        corporate_name_or_jurisdiction_name_as_entry_element=dsl.Field(),
        location_of_meeting=dsl.Field(),
        subordinate_unit=dsl.Field(),
        relator_term=dsl.Field(),
        date_of_meeting_or_treaty_signing=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_of_a_work=dsl.Field(),
        form_subheading=dsl.Field(),
        language_of_a_work=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        number_of_part_section_meeting=dsl.Field(),
        authority_record_control_number=dsl.Field(),
        affiliation=dsl.Field(),
        relator_code=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number_r=dsl.Field(),
        title_of_a_work=dsl.Field(),
    )

    @main_entry_corporate_name.creator('marc', '110..')
    @utils.filter_values
    def main_entry_corporate_name(self, value):
        return {
            'corporate_name_or_jurisdiction_name_as_entry_element': value.get('a'),
            'location_of_meeting': value.get('c'),
            'subordinate_unit': value.get('b'),
            'relator_term': value.get('e'),
            'date_of_meeting_or_treaty_signing': value.get('d'),
            'miscellaneous_information': value.get('g'),
            'date_of_a_work': value.get('f'),
            'form_subheading': value.get('k'),
            'language_of_a_work': value.get('l'),
            'name_of_part_section_of_a_work': value.get('p'),
            'number_of_part_section_meeting': value.get('n'),
            'authority_record_control_number': value.get('0'),
            'affiliation': value.get('u'),
            'relator_code': value.get('4'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number_r': value.get('8'),
            'title_of_a_work': value.get('t')}

    main_entry_meeting_name = dsl.Object(
        meeting_name_or_jurisdiction_name_as_entry_element=dsl.Field(),
        location_of_meeting=dsl.Field(),
        subordinate_unit=dsl.Field(),
        date_of_meeting=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_of_a_work=dsl.Field(),
        form_subheading=dsl.Field(),
        relator_term=dsl.Field(),
        language_of_a_work=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        number_of_part_section_meeting=dsl.Field(),
        name_of_meeting_following_jurisdiction_name_entry_element=dsl.Field(),
        authority_record_control_number=dsl.Field(),
        affiliation=dsl.Field(),
        relator_code=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        title_of_a_work=dsl.Field(),
    )

    @main_entry_meeting_name.creator('marc', '111..')
    @utils.filter_values
    def main_entry_meeting_name(self, value):
        return {
            'meeting_name_or_jurisdiction_name_as_entry_element': value.get('a'),
            'location_of_meeting': value.get('c'),
            'subordinate_unit': value.get('e'),
            'date_of_meeting': value.get('d'),
            'miscellaneous_information': value.get('g'),
            'date_of_a_work': value.get('f'),
            'form_subheading': value.get('k'),
            'relator_term': value.get('j'),
            'language_of_a_work': value.get('l'),
            'name_of_part_section_of_a_work': value.get('p'),
            'number_of_part_section_meeting': value.get('n'),
            'name_of_meeting_following_jurisdiction_name_entry_element': value.get('q'),
            'authority_record_control_number': value.get('0'),
            'affiliation': value.get('u'),
            'relator_code': value.get('4'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'title_of_a_work': value.get('t')}

    main_entry_uniform_title = dsl.Object(
        uniform_title=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        date_of_treaty_signing=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_of_a_work=dsl.Field(),
        medium=dsl.Field(),
        form_subheading=dsl.Field(),
        medium_of_performance_for_music=dsl.Field(),
        language_of_a_work=dsl.Field(),
        arranged_statement_for_music=dsl.Field(),
        number_of_part_section_of_a_work=dsl.Field(),
        authority_record_control_number=dsl.Field(),
        version=dsl.Field(),
        key_for_music=dsl.Field(),
        title_of_a_work=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    )

    @main_entry_uniform_title.creator('marc', '130..')
    @utils.filter_values
    def main_entry_uniform_title(self, value):
        return {
            'uniform_title': value.get('a'),
            'name_of_part_section_of_a_work': value.get('p'),
            'date_of_treaty_signing': value.get('d'),
            'miscellaneous_information': value.get('g'),
            'date_of_a_work': value.get('f'),
            'medium': value.get('h'),
            'form_subheading': value.get('k'),
            'medium_of_performance_for_music': value.get('m'),
            'language_of_a_work': value.get('l'),
            'arranged_statement_for_music': value.get('o'),
            'number_of_part_section_of_a_work': value.get('n'),
            'authority_record_control_number': value.get('0'),
            'version': value.get('s'),
            'key_for_music': value.get('r'),
            'title_of_a_work': value.get('t'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    abbreviated_title = dsl.List(dsl.Object(
        abbreviated_title=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        source=dsl.Field(),
        qualifying_information=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @abbreviated_title.creator('marc', '210..')
    @utils.for_each_value
    @utils.filter_values
    def abbreviated_title(self, value):
        return {
            'abbreviated_title': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'source': value.get('2'),
            'qualifying_information': value.get('b'),
            'linkage': value.get('6')}

    key_title = dsl.List(dsl.Object(
        key_title=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        qualifying_information=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @key_title.creator('marc', '222..')
    @utils.for_each_value
    @utils.filter_values
    def key_title(self, value):
        return {
            'key_title': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'qualifying_information': value.get('b'),
            'linkage': value.get('6')}

    uniform_title = dsl.Object(
        uniform_title=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        date_of_treaty_signing=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_of_a_work=dsl.Field(),
        medium=dsl.Field(),
        form_subheading=dsl.Field(),
        medium_of_performance_for_music=dsl.Field(),
        language_of_a_work=dsl.Field(),
        arranged_statement_for_music=dsl.Field(),
        number_of_part_section_of_a_work=dsl.Field(),
        authority_record_control_number=dsl.Field(),
        version=dsl.Field(),
        key_for_music=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    )

    @uniform_title.creator('marc', '240..')
    @utils.filter_values
    def uniform_title(self, value):
        return {
            'uniform_title': value.get('a'),
            'name_of_part_section_of_a_work': value.get('p'),
            'date_of_treaty_signing': value.get('d'),
            'miscellaneous_information': value.get('g'),
            'date_of_a_work': value.get('f'),
            'medium': value.get('h'),
            'form_subheading': value.get('k'),
            'medium_of_performance_for_music': value.get('m'),
            'language_of_a_work': value.get('l'),
            'arranged_statement_for_music': value.get('o'),
            'number_of_part_section_of_a_work': value.get('n'),
            'authority_record_control_number': value.get('0'),
            'version': value.get('s'),
            'key_for_music': value.get('r'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    translation_of_title_by_cataloging_agency = dsl.List(dsl.Object(
        title=dsl.Field(),
        statement_of_responsibility_=dsl.Field(),
        remainder_of_title=dsl.Field(),
        medium=dsl.Field(),
        number_of_part_section_of_a_work=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        linkage=dsl.Field(),
        language_code_of_translated_title=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @translation_of_title_by_cataloging_agency.creator('marc', '242..')
    @utils.for_each_value
    @utils.filter_values
    def translation_of_title_by_cataloging_agency(self, value):
        return {
            'title': value.get('a'),
            'statement_of_responsibility_': value.get('c'),
            'remainder_of_title': value.get('b'),
            'medium': value.get('h'),
            'number_of_part_section_of_a_work': value.get('n'),
            'name_of_part_section_of_a_work': value.get('p'),
            'linkage': value.get('6'),
            'language_code_of_translated_title': value.get('y'),
            'field_link_and_sequence_number': value.get('8')}

    collective_uniform_title = dsl.Object(
        uniform_title=dsl.Field(),
        date_of_treaty_signing=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_of_a_work=dsl.Field(),
        medium=dsl.Field(),
        form_subheading=dsl.Field(),
        medium_of_performance_for_music=dsl.Field(),
        language_of_a_work=dsl.Field(),
        arranged_statement_for_music=dsl.Field(),
        number_of_part_section_of_a_work=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        version=dsl.Field(),
        key_for_music=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    )

    @collective_uniform_title.creator('marc', '243..')
    @utils.filter_values
    def collective_uniform_title(self, value):
        return {
            'uniform_title': value.get('a'),
            'date_of_treaty_signing': value.get('d'),
            'miscellaneous_information': value.get('g'),
            'date_of_a_work': value.get('f'),
            'medium': value.get('h'),
            'form_subheading': value.get('k'),
            'medium_of_performance_for_music': value.get('m'),
            'language_of_a_work': value.get('l'),
            'arranged_statement_for_music': value.get('o'),
            'number_of_part_section_of_a_work': value.get('n'),
            'name_of_part_section_of_a_work': value.get('p'),
            'version': value.get('s'),
            'key_for_music': value.get('r'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    title_statement = dsl.Object(
        title=dsl.Field(),
        statement_of_responsibility_=dsl.Field(),
        remainder_of_title=dsl.Field(),
        bulk_dates=dsl.Field(),
        inclusive_dates=dsl.Field(),
        medium=dsl.Field(),
        form=dsl.Field(),
        number_of_part_section_of_a_work=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        version=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    )

    @title_statement.creator('marc', '245..')
    @utils.filter_values
    def title_statement(self, value):
        return {
            'title': value.get('a'),
            'statement_of_responsibility_': value.get('c'),
            'remainder_of_title': value.get('b'),
            'bulk_dates': value.get('g'),
            'inclusive_dates': value.get('f'),
            'medium': value.get('h'),
            'form': value.get('k'),
            'number_of_part_section_of_a_work': value.get('n'),
            'name_of_part_section_of_a_work': value.get('p'),
            'version': value.get('s'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    varying_form_of_title = dsl.List(dsl.Object(
        title_proper_short_title=dsl.Field(),
        remainder_of_title=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_or_sequential_designation=dsl.Field(),
        display_text=dsl.Field(),
        medium=dsl.Field(),
        number_of_part_section_of_a_work=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @varying_form_of_title.creator('marc', '246..')
    @utils.for_each_value
    @utils.filter_values
    def varying_form_of_title(self, value):
        return {
            'title_proper_short_title': value.get('a'),
            'remainder_of_title': value.get('b'),
            'miscellaneous_information': value.get('g'),
            'date_or_sequential_designation': value.get('f'),
            'display_text': value.get('i'),
            'medium': value.get('h'),
            'number_of_part_section_of_a_work': value.get('n'),
            'name_of_part_section_of_a_work': value.get('p'),
            'institution_to_which_field_applies': value.get('5'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    former_title = dsl.List(dsl.Object(
        title=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        remainder_of_title=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_or_sequential_designation=dsl.Field(),
        medium=dsl.Field(),
        number_of_part_section_of_a_work=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @former_title.creator('marc', '247..')
    @utils.for_each_value
    @utils.filter_values
    def former_title(self, value):
        return {
            'title': value.get('a'),
            'international_standard_serial_number': value.get('x'),
            'remainder_of_title': value.get('b'),
            'miscellaneous_information': value.get('g'),
            'date_or_sequential_designation': value.get('f'),
            'medium': value.get('h'),
            'number_of_part_section_of_a_work': value.get('n'),
            'name_of_part_section_of_a_work': value.get('p'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    edition_statement = dsl.List(dsl.Object(
        edition_statement=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        materials_specified=dsl.Field(),
        remainder_of_edition_statement=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @edition_statement.creator('marc', '250..')
    @utils.for_each_value
    @utils.filter_values
    def edition_statement(self, value):
        return {
            'edition_statement': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'materials_specified': value.get('3'),
            'remainder_of_edition_statement': value.get('b'),
            'linkage': value.get('6')}

    musical_presentation_statement = dsl.Object(
        musical_presentation_statement=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        linkage=dsl.Field(),
    )

    @musical_presentation_statement.creator('marc', '254..')
    @utils.filter_values
    def musical_presentation_statement(self, value):
        return {
            'musical_presentation_statement': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'linkage': value.get('6')}

    cartographic_mathematical_data = dsl.List(dsl.Object(
        statement_of_scale=dsl.Field(),
        statement_of_coordinates=dsl.Field(),
        statement_of_projection=dsl.Field(),
        statement_of_equinox=dsl.Field(),
        statement_of_zone=dsl.Field(),
        exclusion_g_ring_coordinate_pairs=dsl.Field(),
        outer_g_ring_coordinate_pairs=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @cartographic_mathematical_data.creator('marc', '255..')
    @utils.for_each_value
    @utils.filter_values
    def cartographic_mathematical_data(self, value):
        return {
            'statement_of_scale': value.get('a'),
            'statement_of_coordinates': value.get('c'),
            'statement_of_projection': value.get('b'),
            'statement_of_equinox': value.get('e'),
            'statement_of_zone': value.get('d'),
            'exclusion_g_ring_coordinate_pairs': value.get('g'),
            'outer_g_ring_coordinate_pairs': value.get('f'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    computer_file_characteristics = dsl.Object(
        computer_file_characteristics=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        linkage=dsl.Field(),
    )

    @computer_file_characteristics.creator('marc', '256..')
    @utils.filter_values
    def computer_file_characteristics(self, value):
        return {
            'computer_file_characteristics': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'linkage': value.get('6')}

    country_of_producing_entity = dsl.List(dsl.Object(
        country_of_producing_entity=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        source=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @country_of_producing_entity.creator('marc', '257..')
    @utils.for_each_value
    @utils.filter_values
    def country_of_producing_entity(self, value):
        return {
            'country_of_producing_entity': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'source': value.get('2'),
            'linkage': value.get('6')}

    philatelic_issue_data = dsl.List(dsl.Object(
        issuing_jurisdiction=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        denomination=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @philatelic_issue_data.creator('marc', '258..')
    @utils.for_each_value
    @utils.filter_values
    def philatelic_issue_data(self, value):
        return {
            'issuing_jurisdiction': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'denomination': value.get('b'),
            'linkage': value.get('6')}

    publication_distribution__imprint = dsl.List(dsl.Object(
        place_of_publication_distribution_=dsl.Field(),
        date_of_publication_distribution_=dsl.Field(),
        name_of_publisher_distributor_=dsl.Field(),
        place_of_manufacture=dsl.Field(),
        date_of_manufacture=dsl.Field(),
        manufacturer=dsl.Field(),
        materials_specified=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @publication_distribution__imprint.creator('marc', '260..')
    @utils.for_each_value
    @utils.filter_values
    def publication_distribution__imprint(self, value):
        return {
            'place_of_publication_distribution_': value.get('a'),
            'date_of_publication_distribution_': value.get('c'),
            'name_of_publisher_distributor_': value.get('b'),
            'place_of_manufacture': value.get('e'),
            'date_of_manufacture': value.get('g'),
            'manufacturer': value.get('f'),
            'materials_specified': value.get('3'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    imprint_statement_for_films_pre_aacr_1_revised = dsl.Object(
        producing_company=dsl.Field(),
        releasing_company=dsl.Field(),
        contractual_producer=dsl.Field(),
        date_of_production_release_=dsl.Field(),
        place_of_production_release_=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    )

    @imprint_statement_for_films_pre_aacr_1_revised.creator('marc', '261..')
    @utils.filter_values
    def imprint_statement_for_films_pre_aacr_1_revised(self, value):
        return {
            'producing_company': value.get('a'),
            'releasing_company': value.get('b'),
            'contractual_producer': value.get('e'),
            'date_of_production_release_': value.get('d'),
            'place_of_production_release_': value.get('f'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    imprint_statement_for_sound_recordings_pre_aacr_1 = dsl.Object(
        place_of_production_release_=dsl.Field(),
        date_of_production_release_=dsl.Field(),
        publisher_or_trade_name=dsl.Field(),
        serial_identification=dsl.Field(),
        matrix_and_or_take_number=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    )

    @imprint_statement_for_sound_recordings_pre_aacr_1.creator('marc', '262..')
    @utils.filter_values
    def imprint_statement_for_sound_recordings_pre_aacr_1(self, value):
        return {
            'place_of_production_release_': value.get('a'),
            'date_of_production_release_': value.get('c'),
            'publisher_or_trade_name': value.get('b'),
            'serial_identification': value.get('k'),
            'matrix_and_or_take_number': value.get('l'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    projected_publication_date = dsl.Object(
        projected_publication_date=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        linkage=dsl.Field(),
    )

    @projected_publication_date.creator('marc', '263..')
    @utils.filter_values
    def projected_publication_date(self, value):
        return {
            'projected_publication_date': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'linkage': value.get('6')}

    production_publication_distribution_manufacture_and_copyright_notice = dsl.List(
        dsl.Object(
            place_of_production_publication_distribution_manufacture=dsl.Field(),
            date_of_production_publication_distribution_manufacture_or_copyright_notice=dsl.Field(),
            name_of_producer_publisher_distributor_manufacturer=dsl.Field(),
            materials_specified=dsl.Field(),
            linkage=dsl.Field(),
            field_link_and_sequence_number=dsl.Field(),
        ))

    @production_publication_distribution_manufacture_and_copyright_notice.creator(
        'marc',
        '264..')
    @utils.for_each_value
    @utils.filter_values
    def production_publication_distribution_manufacture_and_copyright_notice(
            self,
            value):
        return {
            'place_of_production_publication_distribution_manufacture': value.get('a'),
            'date_of_production_publication_distribution_manufacture_or_copyright_notice': value.get('c'),
            'name_of_producer_publisher_distributor_manufacturer': value.get('b'),
            'materials_specified': value.get('3'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    address = dsl.List(dsl.Object(
        address=dsl.Field(),
        state_or_province=dsl.Field(),
        city=dsl.Field(),
        postal_code=dsl.Field(),
        country=dsl.Field(),
        attention_name=dsl.Field(),
        terms_preceding_attention_name=dsl.Field(),
        type_of_address=dsl.Field(),
        attention_position=dsl.Field(),
        telephone_number=dsl.Field(),
        specialized_telephone_number=dsl.Field(),
        electronic_mail_address=dsl.Field(),
        fax_number=dsl.Field(),
        tdd_or_tty_number=dsl.Field(),
        title_of_contact_person=dsl.Field(),
        contact_person=dsl.Field(),
        hours=dsl.Field(),
        relator_code=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        public_note=dsl.Field(),
    ))

    @address.creator('marc', '270..')
    @utils.for_each_value
    @utils.filter_values
    def address(self, value):
        return {
            'address': value.get('a'),
            'state_or_province': value.get('c'),
            'city': value.get('b'),
            'postal_code': value.get('e'),
            'country': value.get('d'),
            'attention_name': value.get('g'),
            'terms_preceding_attention_name': value.get('f'),
            'type_of_address': value.get('i'),
            'attention_position': value.get('h'),
            'telephone_number': value.get('k'),
            'specialized_telephone_number': value.get('j'),
            'electronic_mail_address': value.get('m'),
            'fax_number': value.get('l'),
            'tdd_or_tty_number': value.get('n'),
            'title_of_contact_person': value.get('q'),
            'contact_person': value.get('p'),
            'hours': value.get('r'),
            'relator_code': value.get('4'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'public_note': value.get('z')}

    physical_description = dsl.List(dsl.Object(
        extent=dsl.Field(),
        dimensions=dsl.Field(),
        other_physical_details=dsl.Field(),
        accompanying_material=dsl.Field(),
        size_of_unit=dsl.Field(),
        type_of_unit=dsl.Field(),
        materials_specified=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @physical_description.creator('marc', '300..')
    @utils.for_each_value
    @utils.filter_values
    def physical_description(self, value):
        return {
            'extent': value.get('a'),
            'dimensions': value.get('c'),
            'other_physical_details': value.get('b'),
            'accompanying_material': value.get('e'),
            'size_of_unit': value.get('g'),
            'type_of_unit': value.get('f'),
            'materials_specified': value.get('3'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    playing_time = dsl.Object(
        playing_time=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        linkage=dsl.Field(),
    )

    @playing_time.creator('marc', '306..')
    @utils.filter_values
    def playing_time(self, value):
        return {
            'playing_time': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'linkage': value.get('6')}

    hours_ = dsl.List(dsl.Object(
        hours=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        additional_information=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @hours_.creator('marc', '307..')
    @utils.for_each_value
    @utils.filter_values
    def hours_(self, value):
        return {
            'hours': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'additional_information': value.get('b'),
            'linkage': value.get('6')}

    current_publication_frequency = dsl.Object(
        current_publication_frequency=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        date_of_current_publication_frequency=dsl.Field(),
        linkage=dsl.Field(),
    )

    @current_publication_frequency.creator('marc', '310..')
    @utils.filter_values
    def current_publication_frequency(self, value):
        return {
            'current_publication_frequency': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'date_of_current_publication_frequency': value.get('b'),
            'linkage': value.get('6')}

    former_publication_frequency = dsl.List(dsl.Object(
        former_publication_frequency=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        dates_of_former_publication_frequency=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @former_publication_frequency.creator('marc', '321..')
    @utils.for_each_value
    @utils.filter_values
    def former_publication_frequency(self, value):
        return {
            'former_publication_frequency': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'dates_of_former_publication_frequency': value.get('b'),
            'linkage': value.get('6')}

    content_type = dsl.List(dsl.Object(
        content_type_term=dsl.Field(),
        content_type_code=dsl.Field(),
        materials_specified=dsl.Field(),
        source=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @content_type.creator('marc', '336..')
    @utils.for_each_value
    @utils.filter_values
    def content_type(self, value):
        return {
            'content_type_term': value.get('a'),
            'content_type_code': value.get('b'),
            'materials_specified': value.get('3'),
            'source': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    media_type = dsl.List(dsl.Object(
        media_type_term=dsl.Field(),
        media_type_code=dsl.Field(),
        materials_specified=dsl.Field(),
        source=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @media_type.creator('marc', '337..')
    @utils.for_each_value
    @utils.filter_values
    def media_type(self, value):
        return {
            'media_type_term': value.get('a'),
            'media_type_code': value.get('b'),
            'materials_specified': value.get('3'),
            'source': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    carrier_type = dsl.List(dsl.Object(
        carrier_type_term=dsl.Field(),
        carrier_type_code=dsl.Field(),
        materials_specified=dsl.Field(),
        source=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @carrier_type.creator('marc', '338..')
    @utils.for_each_value
    @utils.filter_values
    def carrier_type(self, value):
        return {
            'carrier_type_term': value.get('a'),
            'carrier_type_code': value.get('b'),
            'materials_specified': value.get('3'),
            'source': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    physical_medium = dsl.List(dsl.Object(
        material_base_and_configuration=dsl.Field(),
        materials_applied_to_surface=dsl.Field(),
        dimensions=dsl.Field(),
        support=dsl.Field(),
        information_recording_technique=dsl.Field(),
        production_rate_ratio=dsl.Field(),
        technical_specifications_of_medium=dsl.Field(),
        location_within_medium=dsl.Field(),
        layout=dsl.Field(),
        generation=dsl.Field(),
        book_format=dsl.Field(),
        polarity=dsl.Field(),
        font_size=dsl.Field(),
        authority_record_control_number_or_standard_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @physical_medium.creator('marc', '340..')
    @utils.for_each_value
    @utils.filter_values
    def physical_medium(self, value):
        return {
            'material_base_and_configuration': value.get('a'),
            'materials_applied_to_surface': value.get('c'),
            'dimensions': value.get('b'),
            'support': value.get('e'),
            'information_recording_technique': value.get('d'),
            'production_rate_ratio': value.get('f'),
            'technical_specifications_of_medium': value.get('i'),
            'location_within_medium': value.get('h'),
            'layout': value.get('k'),
            'generation': value.get('j'),
            'book_format': value.get('m'),
            'polarity': value.get('o'),
            'font_size': value.get('n'),
            'authority_record_control_number_or_standard_number': value.get('0'),
            'materials_specified': value.get('3'),
            'source': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    geospatial_reference_data = dsl.List(
        dsl.Object(
            reference_method_used=dsl.Field(),
            linkage=dsl.Field(),
            field_link_and_sequence_number=dsl.Field(),
            name=dsl.Field(),
            latitude_resolution=dsl.Field(),
            coordinate_units_or_distance_units=dsl.Field(),
            standard_parallel_or_oblique_line_latitude=dsl.Field(),
            longitude_resolution=dsl.Field(),
            longitude_of_central_meridian_or_projection_center=dsl.Field(),
            oblique_line_longitude=dsl.Field(),
            false_easting=dsl.Field(),
            latitude_of_projection_center_or_projection_origin=dsl.Field(),
            scale_factor=dsl.Field(),
            false_northing=dsl.Field(),
            azimuthal_angle=dsl.Field(),
            height_of_perspective_point_above_surface=dsl.Field(),
            landsat_number_and_path_number=dsl.Field(),
            azimuth_measure_point_longitude_or_straight_vertical_longitude_from_pole=dsl.Field(),
            ellipsoid_name=dsl.Field(),
            zone_identifier=dsl.Field(),
            denominator_of_flattening_ratio=dsl.Field(),
            semi_major_axis=dsl.Field(),
            vertical_encoding_method=dsl.Field(),
            vertical_resolution=dsl.Field(),
            local_planar_or_local_georeference_information=dsl.Field(),
            local_planar_local_or_other_projection_or_grid_description=dsl.Field(),
        ))

    @geospatial_reference_data.creator('marc', '342..')
    @utils.for_each_value
    @utils.filter_values
    def geospatial_reference_data(self, value):
        return {
            'reference_method_used': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'name': value.get('a'),
            'latitude_resolution': value.get('c'),
            'coordinate_units_or_distance_units': value.get('b'),
            'standard_parallel_or_oblique_line_latitude': value.get('e'),
            'longitude_resolution': value.get('d'),
            'longitude_of_central_meridian_or_projection_center': value.get('g'),
            'oblique_line_longitude': value.get('f'),
            'false_easting': value.get('i'),
            'latitude_of_projection_center_or_projection_origin': value.get('h'),
            'scale_factor': value.get('k'),
            'false_northing': value.get('j'),
            'azimuthal_angle': value.get('m'),
            'height_of_perspective_point_above_surface': value.get('l'),
            'landsat_number_and_path_number': value.get('o'),
            'azimuth_measure_point_longitude_or_straight_vertical_longitude_from_pole': value.get('n'),
            'ellipsoid_name': value.get('q'),
            'zone_identifier': value.get('p'),
            'denominator_of_flattening_ratio': value.get('s'),
            'semi_major_axis': value.get('r'),
            'vertical_encoding_method': value.get('u'),
            'vertical_resolution': value.get('t'),
            'local_planar_or_local_georeference_information': value.get('w'),
            'local_planar_local_or_other_projection_or_grid_description': value.get('v')}

    planar_coordinate_data = dsl.List(dsl.Object(
        planar_coordinate_encoding_method=dsl.Field(),
        abscissa_resolution=dsl.Field(),
        planar_distance_units=dsl.Field(),
        distance_resolution=dsl.Field(),
        ordinate_resolution=dsl.Field(),
        bearing_units=dsl.Field(),
        bearing_resolution=dsl.Field(),
        bearing_reference_meridian=dsl.Field(),
        bearing_reference_direction=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @planar_coordinate_data.creator('marc', '343..')
    @utils.for_each_value
    @utils.filter_values
    def planar_coordinate_data(self, value):
        return {
            'planar_coordinate_encoding_method': value.get('a'),
            'abscissa_resolution': value.get('c'),
            'planar_distance_units': value.get('b'),
            'distance_resolution': value.get('e'),
            'ordinate_resolution': value.get('d'),
            'bearing_units': value.get('g'),
            'bearing_resolution': value.get('f'),
            'bearing_reference_meridian': value.get('i'),
            'bearing_reference_direction': value.get('h'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    sound_characteristics = dsl.List(dsl.Object(
        type_of_recording=dsl.Field(),
        playing_speed=dsl.Field(),
        recording_medium=dsl.Field(),
        track_configuration=dsl.Field(),
        groove_characteristic=dsl.Field(),
        configuration_of_playback_channels=dsl.Field(),
        tape_configuration=dsl.Field(),
        special_playback_characteristics=dsl.Field(),
        authority_record_control_number_or_standard_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @sound_characteristics.creator('marc', '344..')
    @utils.for_each_value
    @utils.filter_values
    def sound_characteristics(self, value):
        return {
            'type_of_recording': value.get('a'),
            'playing_speed': value.get('c'),
            'recording_medium': value.get('b'),
            'track_configuration': value.get('e'),
            'groove_characteristic': value.get('d'),
            'configuration_of_playback_channels': value.get('g'),
            'tape_configuration': value.get('f'),
            'special_playback_characteristics': value.get('h'),
            'authority_record_control_number_or_standard_number': value.get('0'),
            'materials_specified': value.get('3'),
            'source': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    projection_characteristics_of_moving_image = dsl.List(dsl.Object(
        presentation_format=dsl.Field(),
        projection_speed=dsl.Field(),
        authority_record_control_number_or_standard_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @projection_characteristics_of_moving_image.creator('marc', '345..')
    @utils.for_each_value
    @utils.filter_values
    def projection_characteristics_of_moving_image(self, value):
        return {
            'presentation_format': value.get('a'),
            'projection_speed': value.get('b'),
            'authority_record_control_number_or_standard_number': value.get('0'),
            'materials_specified': value.get('3'),
            'source': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    video_characteristics = dsl.List(dsl.Object(
        video_format=dsl.Field(),
        broadcast_standard=dsl.Field(),
        authority_record_control_number_or_standard_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @video_characteristics.creator('marc', '346..')
    @utils.for_each_value
    @utils.filter_values
    def video_characteristics(self, value):
        return {
            'video_format': value.get('a'),
            'broadcast_standard': value.get('b'),
            'authority_record_control_number_or_standard_number': value.get('0'),
            'materials_specified': value.get('3'),
            'source': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    digital_file_characteristics = dsl.List(dsl.Object(
        file_type=dsl.Field(),
        file_size=dsl.Field(),
        encoding_format=dsl.Field(),
        regional_encoding=dsl.Field(),
        resolution=dsl.Field(),
        transmission_speed=dsl.Field(),
        authority_record_control_number_or_standard_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @digital_file_characteristics.creator('marc', '347..')
    @utils.for_each_value
    @utils.filter_values
    def digital_file_characteristics(self, value):
        return {
            'file_type': value.get('a'),
            'file_size': value.get('c'),
            'encoding_format': value.get('b'),
            'regional_encoding': value.get('e'),
            'resolution': value.get('d'),
            'transmission_speed': value.get('f'),
            'authority_record_control_number_or_standard_number': value.get('0'),
            'materials_specified': value.get('3'),
            'source': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    organization_and_arrangement_of_materials = dsl.List(dsl.Object(
        organization=dsl.Field(),
        hierarchical_level=dsl.Field(),
        arrangement=dsl.Field(),
        materials_specified=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @organization_and_arrangement_of_materials.creator('marc', '351..')
    @utils.for_each_value
    @utils.filter_values
    def organization_and_arrangement_of_materials(self, value):
        return {
            'organization': value.get('a'),
            'hierarchical_level': value.get('c'),
            'arrangement': value.get('b'),
            'materials_specified': value.get('3'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    digital_graphic_representation = dsl.List(dsl.Object(
        direct_reference_method=dsl.Field(),
        object_count=dsl.Field(),
        object_type=dsl.Field(),
        column_count=dsl.Field(),
        row_count=dsl.Field(),
        vpf_topology_level=dsl.Field(),
        vertical_count=dsl.Field(),
        indirect_reference_description=dsl.Field(),
        format_of_the_digital_image=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @digital_graphic_representation.creator('marc', '352..')
    @utils.for_each_value
    @utils.filter_values
    def digital_graphic_representation(self, value):
        return {
            'direct_reference_method': value.get('a'),
            'object_count': value.get('c'),
            'object_type': value.get('b'),
            'column_count': value.get('e'),
            'row_count': value.get('d'),
            'vpf_topology_level': value.get('g'),
            'vertical_count': value.get('f'),
            'indirect_reference_description': value.get('i'),
            'format_of_the_digital_image': value.get('q'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    security_classification_control = dsl.List(dsl.Object(
        security_classification=dsl.Field(),
        external_dissemination_information=dsl.Field(),
        handling_instructions=dsl.Field(),
        classification_system=dsl.Field(),
        downgrading_or_declassification_event=dsl.Field(),
        downgrading_date=dsl.Field(),
        country_of_origin_code=dsl.Field(),
        declassification_date=dsl.Field(),
        authorization=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @security_classification_control.creator('marc', '355..')
    @utils.for_each_value
    @utils.filter_values
    def security_classification_control(self, value):
        return {
            'security_classification': value.get('a'),
            'external_dissemination_information': value.get('c'),
            'handling_instructions': value.get('b'),
            'classification_system': value.get('e'),
            'downgrading_or_declassification_event': value.get('d'),
            'downgrading_date': value.get('g'),
            'country_of_origin_code': value.get('f'),
            'declassification_date': value.get('h'),
            'authorization': value.get('j'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    originator_dissemination_control = dsl.Object(
        originator_control_term=dsl.Field(),
        authorized_recipients_of_material=dsl.Field(),
        originating_agency=dsl.Field(),
        other_restrictions=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    )

    @originator_dissemination_control.creator('marc', '357..')
    @utils.filter_values
    def originator_dissemination_control(self, value):
        return {
            'originator_control_term': value.get('a'),
            'authorized_recipients_of_material': value.get('c'),
            'originating_agency': value.get('b'),
            'other_restrictions': value.get('g'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    dates_of_publication_and_or_sequential_designation = dsl.List(dsl.Object(
        dates_of_publication_and_or_sequential_designation=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        source_of_information=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @dates_of_publication_and_or_sequential_designation.creator(
        'marc',
        '362..')
    @utils.for_each_value
    @utils.filter_values
    def dates_of_publication_and_or_sequential_designation(self, value):
        return {
            'dates_of_publication_and_or_sequential_designation': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'source_of_information': value.get('z'),
            'linkage': value.get('6')}

    normalized_date_and_sequential_designation = dsl.List(dsl.Object(
        first_level_of_enumeration=dsl.Field(),
        nonpublic_note=dsl.Field(),
        third_level_of_enumeration=dsl.Field(),
        second_level_of_enumeration=dsl.Field(),
        fifth_level_of_enumeration=dsl.Field(),
        fourth_level_of_enumeration=dsl.Field(),
        alternative_numbering_scheme_first_level_of_enumeration=dsl.Field(),
        sixth_level_of_enumeration=dsl.Field(),
        first_level_of_chronology=dsl.Field(),
        alternative_numbering_scheme_second_level_of_enumeration=dsl.Field(),
        third_level_of_chronology=dsl.Field(),
        second_level_of_chronology=dsl.Field(),
        alternative_numbering_scheme_chronology=dsl.Field(),
        fourth_level_of_chronology=dsl.Field(),
        first_level_textual_designation=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        public_note=dsl.Field(),
        first_level_of_chronology_issuance=dsl.Field(),
    ))

    @normalized_date_and_sequential_designation.creator('marc', '363..')
    @utils.for_each_value
    @utils.filter_values
    def normalized_date_and_sequential_designation(self, value):
        return {
            'first_level_of_enumeration': value.get('a'),
            'nonpublic_note': value.get('x'),
            'third_level_of_enumeration': value.get('c'),
            'second_level_of_enumeration': value.get('b'),
            'fifth_level_of_enumeration': value.get('e'),
            'fourth_level_of_enumeration': value.get('d'),
            'alternative_numbering_scheme_first_level_of_enumeration': value.get('g'),
            'sixth_level_of_enumeration': value.get('f'),
            'first_level_of_chronology': value.get('i'),
            'alternative_numbering_scheme_second_level_of_enumeration': value.get('h'),
            'third_level_of_chronology': value.get('k'),
            'second_level_of_chronology': value.get('j'),
            'alternative_numbering_scheme_chronology': value.get('m'),
            'fourth_level_of_chronology': value.get('l'),
            'first_level_textual_designation': value.get('u'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'public_note': value.get('z'),
            'first_level_of_chronology_issuance': value.get('v')}

    trade_price = dsl.List(dsl.Object(
        price_type_code=dsl.Field(),
        currency_code=dsl.Field(),
        price_amount=dsl.Field(),
        price_note=dsl.Field(),
        unit_of_pricing=dsl.Field(),
        price_effective_until=dsl.Field(),
        price_effective_from=dsl.Field(),
        tax_rate_2=dsl.Field(),
        tax_rate_1=dsl.Field(),
        marc_country_code=dsl.Field(),
        iso_country_code=dsl.Field(),
        identification_of_pricing_entity=dsl.Field(),
        source_of_price_type_code=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @trade_price.creator('marc', '365..')
    @utils.for_each_value
    @utils.filter_values
    def trade_price(self, value):
        return {
            'price_type_code': value.get('a'),
            'currency_code': value.get('c'),
            'price_amount': value.get('b'),
            'price_note': value.get('e'),
            'unit_of_pricing': value.get('d'),
            'price_effective_until': value.get('g'),
            'price_effective_from': value.get('f'),
            'tax_rate_2': value.get('i'),
            'tax_rate_1': value.get('h'),
            'marc_country_code': value.get('k'),
            'iso_country_code': value.get('j'),
            'identification_of_pricing_entity': value.get('m'),
            'source_of_price_type_code': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    trade_availability_information = dsl.List(dsl.Object(
        publishers_compressed_title_identification=dsl.Field(),
        availability_status_code=dsl.Field(),
        detailed_date_of_publication=dsl.Field(),
        note=dsl.Field(),
        expected_next_availability_date=dsl.Field(),
        date_made_out_of_print=dsl.Field(),
        publisher_s_discount_category=dsl.Field(),
        marc_country_code=dsl.Field(),
        iso_country_code=dsl.Field(),
        identification_of_agency=dsl.Field(),
        source_of_availability_status_code=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @trade_availability_information.creator('marc', '366..')
    @utils.for_each_value
    @utils.filter_values
    def trade_availability_information(self, value):
        return {
            'publishers_compressed_title_identification': value.get('a'),
            'availability_status_code': value.get('c'),
            'detailed_date_of_publication': value.get('b'),
            'note': value.get('e'),
            'expected_next_availability_date': value.get('d'),
            'date_made_out_of_print': value.get('g'),
            'publisher_s_discount_category': value.get('f'),
            'marc_country_code': value.get('k'),
            'iso_country_code': value.get('j'),
            'identification_of_agency': value.get('m'),
            'source_of_availability_status_code': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    associated_language = dsl.List(dsl.Object(
        language_code=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        source=dsl.Field(),
        language_term=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @associated_language.creator('marc', '377..')
    @utils.for_each_value
    @utils.filter_values
    def associated_language(self, value):
        return {
            'language_code': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'source': value.get('2'),
            'language_term': value.get('l'),
            'linkage': value.get('6')}

    form_of_work = dsl.List(dsl.Object(
        form_of_work=dsl.Field(),
        record_control_number=dsl.Field(),
        source_of_term=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @form_of_work.creator('marc', '380..')
    @utils.for_each_value
    @utils.filter_values
    def form_of_work(self, value):
        return {
            'form_of_work': value.get('a'),
            'record_control_number': value.get('0'),
            'source_of_term': value.get('2'),
            'field_link_and_sequence_number': value.get('8'),
            'linkage': value.get('6')}

    other_distinguishing_characteristics_of_work_or_expression = dsl.List(
        dsl.Object(
            other_distinguishing_characteristic=dsl.Field(),
            source_of_information=dsl.Field(),
            record_control_number=dsl.Field(),
            source_of_term=dsl.Field(),
            uniform_resource_identifier=dsl.Field(),
            linkage=dsl.Field(),
            field_link_and_sequence_number=dsl.Field(),))

    @other_distinguishing_characteristics_of_work_or_expression.creator(
        'marc',
        '381..')
    @utils.for_each_value
    @utils.filter_values
    def other_distinguishing_characteristics_of_work_or_expression(
            self,
            value):
        return {
            'other_distinguishing_characteristic': value.get('a'),
            'source_of_information': value.get('v'),
            'record_control_number': value.get('0'),
            'source_of_term': value.get('2'),
            'uniform_resource_identifier': value.get('u'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    medium_of_performance = dsl.List(dsl.Object(
        medium_of_performance=dsl.Field(),
        soloist=dsl.Field(),
        doubling_instrument=dsl.Field(),
        alternative_medium_of_performance=dsl.Field(),
        note=dsl.Field(),
        number_of_performers_of_the_same_medium=dsl.Field(),
        authority_record_control_number_or_standard_number=dsl.Field(),
        total_number_of_performers=dsl.Field(),
        source_of_term=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @medium_of_performance.creator('marc', '382..')
    @utils.for_each_value
    @utils.filter_values
    def medium_of_performance(self, value):
        return {
            'medium_of_performance': value.get('a'),
            'soloist': value.get('b'),
            'doubling_instrument': value.get('d'),
            'alternative_medium_of_performance': value.get('p'),
            'note': value.get('v'),
            'number_of_performers_of_the_same_medium': value.get('n'),
            'authority_record_control_number_or_standard_number': value.get('0'),
            'total_number_of_performers': value.get('s'),
            'source_of_term': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    numeric_designation_of_musical_work = dsl.List(dsl.Object(
        serial_number=dsl.Field(),
        thematic_index_number=dsl.Field(),
        opus_number=dsl.Field(),
        publisher_associated_with_opus_number=dsl.Field(),
        thematic_index_code=dsl.Field(),
        source=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @numeric_designation_of_musical_work.creator('marc', '383..')
    @utils.for_each_value
    @utils.filter_values
    def numeric_designation_of_musical_work(self, value):
        return {
            'serial_number': value.get('a'),
            'thematic_index_number': value.get('c'),
            'opus_number': value.get('b'),
            'publisher_associated_with_opus_number': value.get('e'),
            'thematic_index_code': value.get('d'),
            'source': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    key = dsl.Object(
        key=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        linkage=dsl.Field(),
    )

    @key.creator('marc', '384..')
    @utils.filter_values
    def key(self, value):
        return {
            'key': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'linkage': value.get('6')}

    audience_characteristics = dsl.List(dsl.Object(
        audience_term=dsl.Field(),
        audience_code=dsl.Field(),
        demographic_group_term=dsl.Field(),
        demographic_group_code=dsl.Field(),
        authority_record_control_number_or_standard_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @audience_characteristics.creator('marc', '385..')
    @utils.for_each_value
    @utils.filter_values
    def audience_characteristics(self, value):
        return {
            'audience_term': value.get('a'),
            'audience_code': value.get('b'),
            'demographic_group_term': value.get('m'),
            'demographic_group_code': value.get('n'),
            'authority_record_control_number_or_standard_number': value.get('0'),
            'materials_specified': value.get('3'),
            'source': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    creator_contributor_characteristics = dsl.List(dsl.Object(
        creator_contributor_term=dsl.Field(),
        creator_contributor_code=dsl.Field(),
        demographic_group_term=dsl.Field(),
        demographic_group_code=dsl.Field(),
        authority_record_control_number_or_standard_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @creator_contributor_characteristics.creator('marc', '386..')
    @utils.for_each_value
    @utils.filter_values
    def creator_contributor_characteristics(self, value):
        return {
            'creator_contributor_term': value.get('a'),
            'creator_contributor_code': value.get('b'),
            'demographic_group_term': value.get('m'),
            'demographic_group_code': value.get('n'),
            'authority_record_control_number_or_standard_number': value.get('0'),
            'materials_specified': value.get('3'),
            'source': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    series_statement_added_entry_personal_name = dsl.List(dsl.Object(
        personal_name=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        titles_and_other_words_associated_with_a_name=dsl.Field(),
        numeration=dsl.Field(),
        relator_term=dsl.Field(),
        dates_associated_with_a_name=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_of_a_work=dsl.Field(),
        form_subheading=dsl.Field(),
        volume_sequential_designation=dsl.Field(),
        language_of_a_work=dsl.Field(),
        number_of_part_section_of_a_work=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        affiliation=dsl.Field(),
        relator_code=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        title_of_a_work=dsl.Field(),
    ))

    @series_statement_added_entry_personal_name.creator('marc', '400..')
    @utils.for_each_value
    @utils.filter_values
    def series_statement_added_entry_personal_name(self, value):
        return {
            'personal_name': value.get('a'),
            'international_standard_serial_number': value.get('x'),
            'titles_and_other_words_associated_with_a_name': value.get('c'),
            'numeration': value.get('b'),
            'relator_term': value.get('e'),
            'dates_associated_with_a_name': value.get('d'),
            'miscellaneous_information': value.get('g'),
            'date_of_a_work': value.get('f'),
            'form_subheading': value.get('k'),
            'volume_sequential_designation': value.get('v'),
            'language_of_a_work': value.get('l'),
            'number_of_part_section_of_a_work': value.get('n'),
            'name_of_part_section_of_a_work': value.get('p'),
            'affiliation': value.get('u'),
            'relator_code': value.get('4'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'title_of_a_work': value.get('t')}

    series_statement_added_entry_corporate_name = dsl.List(dsl.Object(
        corporate_name_or_jurisdiction_name_as_entry_element=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        location_of_meeting=dsl.Field(),
        subordinate_unit=dsl.Field(),
        relator_term=dsl.Field(),
        date_of_meeting_or_treaty_signing=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_of_a_work=dsl.Field(),
        form_subheading=dsl.Field(),
        volume_sequential_designation=dsl.Field(),
        language_of_a_work=dsl.Field(),
        number_of_part_section_meeting=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        affiliation=dsl.Field(),
        relator_code=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        title_of_a_work=dsl.Field(),
    ))

    @series_statement_added_entry_corporate_name.creator('marc', '410..')
    @utils.for_each_value
    @utils.filter_values
    def series_statement_added_entry_corporate_name(self, value):
        return {
            'corporate_name_or_jurisdiction_name_as_entry_element': value.get('a'),
            'international_standard_serial_number': value.get('x'),
            'location_of_meeting': value.get('c'),
            'subordinate_unit': value.get('b'),
            'relator_term': value.get('e'),
            'date_of_meeting_or_treaty_signing': value.get('d'),
            'miscellaneous_information': value.get('g'),
            'date_of_a_work': value.get('f'),
            'form_subheading': value.get('k'),
            'volume_sequential_designation': value.get('v'),
            'language_of_a_work': value.get('l'),
            'number_of_part_section_meeting': value.get('n'),
            'name_of_part_section_of_a_work': value.get('p'),
            'affiliation': value.get('u'),
            'relator_code': value.get('4'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'title_of_a_work': value.get('t')}

    series_statement_added_entry_meeting_name = dsl.List(dsl.Object(
        meeting_name_or_jurisdiction_name_as_entry_element=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        location_of_meeting=dsl.Field(),
        subordinate_unit=dsl.Field(),
        date_of_meeting=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_of_a_work=dsl.Field(),
        form_subheading=dsl.Field(),
        volume_sequential_designation=dsl.Field(),
        language_of_a_work=dsl.Field(),
        number_of_part_section_meeting=dsl.Field(),
        name_of_meeting_following_jurisdiction_name_entry_element=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        affiliation=dsl.Field(),
        relator_code=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        title_of_a_work=dsl.Field(),
    ))

    @series_statement_added_entry_meeting_name.creator('marc', '411..')
    @utils.for_each_value
    @utils.filter_values
    def series_statement_added_entry_meeting_name(self, value):
        return {
            'meeting_name_or_jurisdiction_name_as_entry_element': value.get('a'),
            'international_standard_serial_number': value.get('x'),
            'location_of_meeting': value.get('c'),
            'subordinate_unit': value.get('e'),
            'date_of_meeting': value.get('d'),
            'miscellaneous_information': value.get('g'),
            'date_of_a_work': value.get('f'),
            'form_subheading': value.get('k'),
            'volume_sequential_designation': value.get('v'),
            'language_of_a_work': value.get('l'),
            'number_of_part_section_meeting': value.get('n'),
            'name_of_meeting_following_jurisdiction_name_entry_element': value.get('q'),
            'name_of_part_section_of_a_work': value.get('p'),
            'affiliation': value.get('u'),
            'relator_code': value.get('4'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'title_of_a_work': value.get('t')}

    series_statement_added_entry_title = dsl.List(dsl.Object(
        title=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        volume_sequential_designation=dsl.Field(),
        number_of_part_section_of_a_work=dsl.Field(),
        authority_record_control_number=dsl.Field(),
        bibliographic_record_control_number=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @series_statement_added_entry_title.creator('marc', '440..')
    @utils.for_each_value
    @utils.filter_values
    def series_statement_added_entry_title(self, value):
        return {
            'title': value.get('a'),
            'international_standard_serial_number': value.get('x'),
            'name_of_part_section_of_a_work': value.get('p'),
            'volume_sequential_designation': value.get('v'),
            'number_of_part_section_of_a_work': value.get('n'),
            'authority_record_control_number': value.get('0'),
            'bibliographic_record_control_number': value.get('w'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    series_statement = dsl.List(dsl.Object(
        series_statement=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        linkage=dsl.Field(),
        library_of_congress_call_number=dsl.Field(),
        materials_specified=dsl.Field(),
        volume_sequential_designation=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @series_statement.creator('marc', '490..')
    @utils.for_each_value
    @utils.filter_values
    def series_statement(self, value):
        return {
            'series_statement': value.get('a'),
            'international_standard_serial_number': value.get('x'),
            'linkage': value.get('6'),
            'library_of_congress_call_number': value.get('l'),
            'materials_specified': value.get('3'),
            'volume_sequential_designation': value.get('v'),
            'field_link_and_sequence_number': value.get('8')}

    general_note = dsl.List(dsl.Object(
        general_note=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        materials_specified=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @general_note.creator('marc', '500..')
    @utils.for_each_value
    @utils.filter_values
    def general_note(self, value):
        return {
            'general_note': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'materials_specified': value.get('3'),
            'institution_to_which_field_applies': value.get('5'),
            'linkage': value.get('6')}

    with_note = dsl.List(dsl.Object(
        with_note=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @with_note.creator('marc', '501..')
    @utils.for_each_value
    @utils.filter_values
    def with_note(self, value):
        return {
            'with_note': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'institution_to_which_field_applies': value.get('5'),
            'linkage': value.get('6')}

    dissertation_note = dsl.List(dsl.Object(
        dissertation_note=dsl.Field(),
        name_of_granting_institution=dsl.Field(),
        degree_type=dsl.Field(),
        year_degree_granted=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        dissertation_identifier=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @dissertation_note.creator('marc', '502..')
    @utils.for_each_value
    @utils.filter_values
    def dissertation_note(self, value):
        return {
            'dissertation_note': value.get('a'),
            'name_of_granting_institution': value.get('c'),
            'degree_type': value.get('b'),
            'year_degree_granted': value.get('d'),
            'miscellaneous_information': value.get('g'),
            'dissertation_identifier': value.get('o'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    bibliography__note = dsl.List(dsl.Object(
        bibliography__note=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        number_of_references=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @bibliography__note.creator('marc', '504..')
    @utils.for_each_value
    @utils.filter_values
    def bibliography__note(self, value):
        return {
            'bibliography__note': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'number_of_references': value.get('b'),
            'linkage': value.get('6')}

    formatted_contents_note = dsl.List(dsl.Object(
        formatted_contents_note=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        statement_of_responsibility=dsl.Field(),
        uniform_resource_identifier=dsl.Field(),
        title=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @formatted_contents_note.creator('marc', '505..')
    @utils.for_each_value
    @utils.filter_values
    def formatted_contents_note(self, value):
        return {
            'formatted_contents_note': value.get('a'),
            'miscellaneous_information': value.get('g'),
            'statement_of_responsibility': value.get('r'),
            'uniform_resource_identifier': value.get('u'),
            'title': value.get('t'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    restrictions_on_access_note = dsl.List(dsl.Object(
        terms_governing_access=dsl.Field(),
        physical_access_provisions=dsl.Field(),
        jurisdiction=dsl.Field(),
        authorization=dsl.Field(),
        authorized_users=dsl.Field(),
        standardized_terminology_for_access_restriction=dsl.Field(),
        materials_specified=dsl.Field(),
        source_of_term=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        uniform_resource_identifier=dsl.Field(),
    ))

    @restrictions_on_access_note.creator('marc', '506..')
    @utils.for_each_value
    @utils.filter_values
    def restrictions_on_access_note(self, value):
        return {
            'terms_governing_access': value.get('a'),
            'physical_access_provisions': value.get('c'),
            'jurisdiction': value.get('b'),
            'authorization': value.get('e'),
            'authorized_users': value.get('d'),
            'standardized_terminology_for_access_restriction': value.get('f'),
            'materials_specified': value.get('3'),
            'source_of_term': value.get('2'),
            'institution_to_which_field_applies': value.get('5'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'uniform_resource_identifier': value.get('u')}

    scale_note_for_graphic_material = dsl.Object(
        representative_fraction_of_scale_note=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        remainder_of_scale_note=dsl.Field(),
        linkage=dsl.Field(),
    )

    @scale_note_for_graphic_material.creator('marc', '507..')
    @utils.filter_values
    def scale_note_for_graphic_material(self, value):
        return {
            'representative_fraction_of_scale_note': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'remainder_of_scale_note': value.get('b'),
            'linkage': value.get('6')}

    creation_production_credits_note = dsl.List(dsl.Object(
        creation_production_credits_note=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @creation_production_credits_note.creator('marc', '508..')
    @utils.for_each_value
    @utils.filter_values
    def creation_production_credits_note(self, value):
        return {
            'creation_production_credits_note': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'linkage': value.get('6')}

    citation_references_note = dsl.List(dsl.Object(
        name_of_source=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        location_within_source=dsl.Field(),
        coverage_of_source=dsl.Field(),
        materials_specified=dsl.Field(),
        uniform_resource_identifier=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @citation_references_note.creator('marc', '510..')
    @utils.for_each_value
    @utils.filter_values
    def citation_references_note(self, value):
        return {
            'name_of_source': value.get('a'),
            'international_standard_serial_number': value.get('x'),
            'location_within_source': value.get('c'),
            'coverage_of_source': value.get('b'),
            'materials_specified': value.get('3'),
            'uniform_resource_identifier': value.get('u'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    participant_or_performer_note = dsl.List(dsl.Object(
        participant_or_performer_note=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @participant_or_performer_note.creator('marc', '511..')
    @utils.for_each_value
    @utils.filter_values
    def participant_or_performer_note(self, value):
        return {
            'participant_or_performer_note': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'linkage': value.get('6')}

    type_of_report_and_period_covered_note = dsl.List(dsl.Object(
        type_of_report=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        period_covered=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @type_of_report_and_period_covered_note.creator('marc', '513..')
    @utils.for_each_value
    @utils.filter_values
    def type_of_report_and_period_covered_note(self, value):
        return {
            'type_of_report': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'period_covered': value.get('b'),
            'linkage': value.get('6')}

    data_quality_note = dsl.Object(
        attribute_accuracy_report=dsl.Field(),
        attribute_accuracy_explanation=dsl.Field(),
        attribute_accuracy_value=dsl.Field(),
        completeness_report=dsl.Field(),
        logical_consistency_report=dsl.Field(),
        horizontal_position_accuracy_value=dsl.Field(),
        horizontal_position_accuracy_report=dsl.Field(),
        vertical_positional_accuracy_report=dsl.Field(),
        horizontal_position_accuracy_explanation=dsl.Field(),
        vertical_positional_accuracy_explanation=dsl.Field(),
        vertical_positional_accuracy_value=dsl.Field(),
        cloud_cover=dsl.Field(),
        uniform_resource_identifier=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        display_note=dsl.Field(),
    )

    @data_quality_note.creator('marc', '514..')
    @utils.filter_values
    def data_quality_note(self, value):
        return {
            'attribute_accuracy_report': value.get('a'),
            'attribute_accuracy_explanation': value.get('c'),
            'attribute_accuracy_value': value.get('b'),
            'completeness_report': value.get('e'),
            'logical_consistency_report': value.get('d'),
            'horizontal_position_accuracy_value': value.get('g'),
            'horizontal_position_accuracy_report': value.get('f'),
            'vertical_positional_accuracy_report': value.get('i'),
            'horizontal_position_accuracy_explanation': value.get('h'),
            'vertical_positional_accuracy_explanation': value.get('k'),
            'vertical_positional_accuracy_value': value.get('j'),
            'cloud_cover': value.get('m'),
            'uniform_resource_identifier': value.get('u'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'display_note': value.get('z')}

    numbering_peculiarities_note = dsl.List(dsl.Object(
        numbering_peculiarities_note=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @numbering_peculiarities_note.creator('marc', '515..')
    @utils.for_each_value
    @utils.filter_values
    def numbering_peculiarities_note(self, value):
        return {
            'numbering_peculiarities_note': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'linkage': value.get('6')}

    type_of_computer_file_or_data_note = dsl.List(dsl.Object(
        type_of_computer_file_or_data_note=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @type_of_computer_file_or_data_note.creator('marc', '516..')
    @utils.for_each_value
    @utils.filter_values
    def type_of_computer_file_or_data_note(self, value):
        return {
            'type_of_computer_file_or_data_note': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'linkage': value.get('6')}

    date_time_and_place_of_an_event_note = dsl.List(dsl.Object(
        date_time_and_place_of_an_event_note=dsl.Field(),
        date_of_event=dsl.Field(),
        place_of_event=dsl.Field(),
        other_event_information=dsl.Field(),
        record_control_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source_of_term=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @date_time_and_place_of_an_event_note.creator('marc', '518..')
    @utils.for_each_value
    @utils.filter_values
    def date_time_and_place_of_an_event_note(self, value):
        return {
            'date_time_and_place_of_an_event_note': value.get('a'),
            'date_of_event': value.get('d'),
            'place_of_event': value.get('p'),
            'other_event_information': value.get('o'),
            'record_control_number': value.get('0'),
            'materials_specified': value.get('3'),
            'source_of_term': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    summary_ = dsl.List(dsl.Object(
        summary_=dsl.Field(),
        assigning_source=dsl.Field(),
        expansion_of_summary_note=dsl.Field(),
        materials_specified=dsl.Field(),
        source=dsl.Field(),
        uniform_resource_identifier=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @summary_.creator('marc', '520..')
    @utils.for_each_value
    @utils.filter_values
    def summary_(self, value):
        return {
            'summary_': value.get('a'),
            'assigning_source': value.get('c'),
            'expansion_of_summary_note': value.get('b'),
            'materials_specified': value.get('3'),
            'source': value.get('2'),
            'uniform_resource_identifier': value.get('u'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    target_audience_note = dsl.List(dsl.Object(
        target_audience_note=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @target_audience_note.creator('marc', '521..')
    @utils.for_each_value
    @utils.filter_values
    def target_audience_note(self, value):
        return {
            'target_audience_note': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'materials_specified': value.get('3'),
            'source': value.get('b'),
            'linkage': value.get('6')}

    geographic_coverage_note = dsl.List(dsl.Object(
        geographic_coverage_note=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @geographic_coverage_note.creator('marc', '522..')
    @utils.for_each_value
    @utils.filter_values
    def geographic_coverage_note(self, value):
        return {
            'geographic_coverage_note': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'linkage': value.get('6')}

    preferred_citation_of_described_materials_note = dsl.List(dsl.Object(
        preferred_citation_of_described_materials_note=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source_of_schema_used=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @preferred_citation_of_described_materials_note.creator('marc', '524..')
    @utils.for_each_value
    @utils.filter_values
    def preferred_citation_of_described_materials_note(self, value):
        return {
            'preferred_citation_of_described_materials_note': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'materials_specified': value.get('3'),
            'source_of_schema_used': value.get('2'),
            'linkage': value.get('6')}

    supplement_note = dsl.List(dsl.Object(
        supplement_note=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @supplement_note.creator('marc', '525..')
    @utils.for_each_value
    @utils.filter_values
    def supplement_note(self, value):
        return {
            'supplement_note': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'linkage': value.get('6')}

    study_program_information_note = dsl.List(dsl.Object(
        program_name=dsl.Field(),
        nonpublic_note=dsl.Field(),
        reading_level=dsl.Field(),
        interest_level=dsl.Field(),
        title_point_value=dsl.Field(),
        display_text=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        public_note=dsl.Field(),
    ))

    @study_program_information_note.creator('marc', '526..')
    @utils.for_each_value
    @utils.filter_values
    def study_program_information_note(self, value):
        return {
            'program_name': value.get('a'),
            'nonpublic_note': value.get('x'),
            'reading_level': value.get('c'),
            'interest_level': value.get('b'),
            'title_point_value': value.get('d'),
            'display_text': value.get('i'),
            'institution_to_which_field_applies': value.get('5'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'public_note': value.get('z')}

    additional_physical_form_available_note = dsl.List(dsl.Object(
        additional_physical_form_available_note=dsl.Field(),
        availability_conditions=dsl.Field(),
        availability_source=dsl.Field(),
        order_number=dsl.Field(),
        materials_specified=dsl.Field(),
        uniform_resource_identifier=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @additional_physical_form_available_note.creator('marc', '530..')
    @utils.for_each_value
    @utils.filter_values
    def additional_physical_form_available_note(self, value):
        return {
            'additional_physical_form_available_note': value.get('a'),
            'availability_conditions': value.get('c'),
            'availability_source': value.get('b'),
            'order_number': value.get('d'),
            'materials_specified': value.get('3'),
            'uniform_resource_identifier': value.get('u'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    reproduction_note = dsl.List(dsl.Object(
        type_of_reproduction=dsl.Field(),
        agency_responsible_for_reproduction=dsl.Field(),
        place_of_reproduction=dsl.Field(),
        physical_description_of_reproduction=dsl.Field(),
        date_of_reproduction=dsl.Field(),
        series_statement_of_reproduction=dsl.Field(),
        dates_and_or_sequential_designation_of_issues_reproduced=dsl.Field(),
        note_about_reproduction=dsl.Field(),
        materials_specified=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        fixed_length_data_elements_of_reproduction=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @reproduction_note.creator('marc', '533..')
    @utils.for_each_value
    @utils.filter_values
    def reproduction_note(self, value):
        return {
            'type_of_reproduction': value.get('a'),
            'agency_responsible_for_reproduction': value.get('c'),
            'place_of_reproduction': value.get('b'),
            'physical_description_of_reproduction': value.get('e'),
            'date_of_reproduction': value.get('d'),
            'series_statement_of_reproduction': value.get('f'),
            'dates_and_or_sequential_designation_of_issues_reproduced': value.get('m'),
            'note_about_reproduction': value.get('n'),
            'materials_specified': value.get('3'),
            'institution_to_which_field_applies': value.get('5'),
            'fixed_length_data_elements_of_reproduction': value.get('7'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    original_version_note = dsl.List(dsl.Object(
        main_entry_of_original=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        publication_distribution__of_original=dsl.Field(),
        edition_statement_of_original=dsl.Field(),
        physical_description__of_original=dsl.Field(),
        series_statement_of_original=dsl.Field(),
        key_title_of_original=dsl.Field(),
        material_specific_details=dsl.Field(),
        location_of_original=dsl.Field(),
        other_resource_identifier=dsl.Field(),
        note_about_original=dsl.Field(),
        introductory_phrase=dsl.Field(),
        materials_specified=dsl.Field(),
        title_statement_of_original=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        international_standard_book_number=dsl.Field(),
    ))

    @original_version_note.creator('marc', '534..')
    @utils.for_each_value
    @utils.filter_values
    def original_version_note(self, value):
        return {
            'main_entry_of_original': value.get('a'),
            'international_standard_serial_number': value.get('x'),
            'publication_distribution__of_original': value.get('c'),
            'edition_statement_of_original': value.get('b'),
            'physical_description__of_original': value.get('e'),
            'series_statement_of_original': value.get('f'),
            'key_title_of_original': value.get('k'),
            'material_specific_details': value.get('m'),
            'location_of_original': value.get('l'),
            'other_resource_identifier': value.get('o'),
            'note_about_original': value.get('n'),
            'introductory_phrase': value.get('p'),
            'materials_specified': value.get('3'),
            'title_statement_of_original': value.get('t'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'international_standard_book_number': value.get('z')}

    location_of_originals_duplicates_note = dsl.List(dsl.Object(
        custodian=dsl.Field(),
        country=dsl.Field(),
        postal_address=dsl.Field(),
        telecommunications_address=dsl.Field(),
        repository_location_code=dsl.Field(),
        materials_specified=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @location_of_originals_duplicates_note.creator('marc', '535..')
    @utils.for_each_value
    @utils.filter_values
    def location_of_originals_duplicates_note(self, value):
        return {
            'custodian': value.get('a'),
            'country': value.get('c'),
            'postal_address': value.get('b'),
            'telecommunications_address': value.get('d'),
            'repository_location_code': value.get('g'),
            'materials_specified': value.get('3'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    funding_information_note = dsl.List(dsl.Object(
        text_of_note=dsl.Field(),
        grant_number=dsl.Field(),
        contract_number=dsl.Field(),
        program_element_number=dsl.Field(),
        undifferentiated_number=dsl.Field(),
        task_number=dsl.Field(),
        project_number=dsl.Field(),
        work_unit_number=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @funding_information_note.creator('marc', '536..')
    @utils.for_each_value
    @utils.filter_values
    def funding_information_note(self, value):
        return {
            'text_of_note': value.get('a'),
            'grant_number': value.get('c'),
            'contract_number': value.get('b'),
            'program_element_number': value.get('e'),
            'undifferentiated_number': value.get('d'),
            'task_number': value.get('g'),
            'project_number': value.get('f'),
            'work_unit_number': value.get('h'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    system_details_note = dsl.List(dsl.Object(
        system_details_note=dsl.Field(),
        display_text=dsl.Field(),
        materials_specified=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        uniform_resource_identifier=dsl.Field(),
    ))

    @system_details_note.creator('marc', '538..')
    @utils.for_each_value
    @utils.filter_values
    def system_details_note(self, value):
        return {
            'system_details_note': value.get('a'),
            'display_text': value.get('i'),
            'materials_specified': value.get('3'),
            'institution_to_which_field_applies': value.get('5'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'uniform_resource_identifier': value.get('u')}

    terms_governing_use_and_reproduction_note = dsl.List(dsl.Object(
        terms_governing_use_and_reproduction=dsl.Field(),
        authorization=dsl.Field(),
        jurisdiction=dsl.Field(),
        authorized_users=dsl.Field(),
        materials_specified=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        uniform_resource_identifier=dsl.Field(),
    ))

    @terms_governing_use_and_reproduction_note.creator('marc', '540..')
    @utils.for_each_value
    @utils.filter_values
    def terms_governing_use_and_reproduction_note(self, value):
        return {
            'terms_governing_use_and_reproduction': value.get('a'),
            'authorization': value.get('c'),
            'jurisdiction': value.get('b'),
            'authorized_users': value.get('d'),
            'materials_specified': value.get('3'),
            'institution_to_which_field_applies': value.get('5'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'uniform_resource_identifier': value.get('u')}

    immediate_source_of_acquisition_note = dsl.List(dsl.Object(
        source_of_acquisition=dsl.Field(),
        method_of_acquisition=dsl.Field(),
        address=dsl.Field(),
        accession_number=dsl.Field(),
        date_of_acquisition=dsl.Field(),
        owner=dsl.Field(),
        purchase_price=dsl.Field(),
        type_of_unit=dsl.Field(),
        extent=dsl.Field(),
        materials_specified=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @immediate_source_of_acquisition_note.creator('marc', '541..')
    @utils.for_each_value
    @utils.filter_values
    def immediate_source_of_acquisition_note(self, value):
        return {
            'source_of_acquisition': value.get('a'),
            'method_of_acquisition': value.get('c'),
            'address': value.get('b'),
            'accession_number': value.get('e'),
            'date_of_acquisition': value.get('d'),
            'owner': value.get('f'),
            'purchase_price': value.get('h'),
            'type_of_unit': value.get('o'),
            'extent': value.get('n'),
            'materials_specified': value.get('3'),
            'institution_to_which_field_applies': value.get('5'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    information_relating_to_copyright_status = dsl.List(dsl.Object(
        materials_specified=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        personal_creator=dsl.Field(),
        corporate_creator=dsl.Field(),
        personal_creator_death_date=dsl.Field(),
        copyright_holder_contact_information=dsl.Field(),
        copyright_holder=dsl.Field(),
        copyright_date=dsl.Field(),
        copyright_statement=dsl.Field(),
        publication_date=dsl.Field(),
        copyright_renewal_date=dsl.Field(),
        publisher=dsl.Field(),
        creation_date=dsl.Field(),
        publication_status=dsl.Field(),
        copyright_status=dsl.Field(),
        research_date=dsl.Field(),
        note=dsl.Field(),
        supplying_agency=dsl.Field(),
        country_of_publication_or_creation=dsl.Field(),
        source_of_information=dsl.Field(),
        jurisdiction_of_copyright_assessment=dsl.Field(),
        uniform_resource_identifier=dsl.Field(),
    ))

    @information_relating_to_copyright_status.creator('marc', '542..')
    @utils.for_each_value
    @utils.filter_values
    def information_relating_to_copyright_status(self, value):
        return {
            'materials_specified': value.get('3'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'personal_creator': value.get('a'),
            'corporate_creator': value.get('c'),
            'personal_creator_death_date': value.get('b'),
            'copyright_holder_contact_information': value.get('e'),
            'copyright_holder': value.get('d'),
            'copyright_date': value.get('g'),
            'copyright_statement': value.get('f'),
            'publication_date': value.get('i'),
            'copyright_renewal_date': value.get('h'),
            'publisher': value.get('k'),
            'creation_date': value.get('j'),
            'publication_status': value.get('m'),
            'copyright_status': value.get('l'),
            'research_date': value.get('o'),
            'note': value.get('n'),
            'supplying_agency': value.get('q'),
            'country_of_publication_or_creation': value.get('p'),
            'source_of_information': value.get('s'),
            'jurisdiction_of_copyright_assessment': value.get('r'),
            'uniform_resource_identifier': value.get('u')}

    location_of_other_archival_materials_note = dsl.List(dsl.Object(
        custodian=dsl.Field(),
        country=dsl.Field(),
        address=dsl.Field(),
        provenance=dsl.Field(),
        title=dsl.Field(),
        note=dsl.Field(),
        materials_specified=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @location_of_other_archival_materials_note.creator('marc', '544..')
    @utils.for_each_value
    @utils.filter_values
    def location_of_other_archival_materials_note(self, value):
        return {
            'custodian': value.get('a'),
            'country': value.get('c'),
            'address': value.get('b'),
            'provenance': value.get('e'),
            'title': value.get('d'),
            'note': value.get('n'),
            'materials_specified': value.get('3'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    biographical_or_historical_data = dsl.List(dsl.Object(
        biographical_or_historical_data=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        expansion=dsl.Field(),
        uniform_resource_identifier=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @biographical_or_historical_data.creator('marc', '545..')
    @utils.for_each_value
    @utils.filter_values
    def biographical_or_historical_data(self, value):
        return {
            'biographical_or_historical_data': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'expansion': value.get('b'),
            'uniform_resource_identifier': value.get('u'),
            'linkage': value.get('6')}

    language_note = dsl.List(dsl.Object(
        language_note=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        materials_specified=dsl.Field(),
        information_code_or_alphabet=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @language_note.creator('marc', '546..')
    @utils.for_each_value
    @utils.filter_values
    def language_note(self, value):
        return {
            'language_note': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'materials_specified': value.get('3'),
            'information_code_or_alphabet': value.get('b'),
            'linkage': value.get('6')}

    former_title_complexity_note = dsl.List(dsl.Object(
        former_title_complexity_note=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @former_title_complexity_note.creator('marc', '547..')
    @utils.for_each_value
    @utils.filter_values
    def former_title_complexity_note(self, value):
        return {
            'former_title_complexity_note': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'linkage': value.get('6')}

    issuing_body_note = dsl.List(dsl.Object(
        issuing_body_note=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @issuing_body_note.creator('marc', '550..')
    @utils.for_each_value
    @utils.filter_values
    def issuing_body_note(self, value):
        return {
            'issuing_body_note': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'linkage': value.get('6')}

    entity_and_attribute_information_note = dsl.List(dsl.Object(
        entity_type_label=dsl.Field(),
        attribute_label=dsl.Field(),
        entity_type_definition_and_source=dsl.Field(),
        enumerated_domain_value=dsl.Field(),
        attribute_definition_and_source=dsl.Field(),
        range_domain_minimum_and_maximum=dsl.Field(),
        enumerated_domain_value_definition_and_source=dsl.Field(),
        unrepresentable_domain=dsl.Field(),
        codeset_name_and_source=dsl.Field(),
        beginning_and_ending_date_of_attribute_values=dsl.Field(),
        attribute_units_of_measurement_and_resolution=dsl.Field(),
        attribute_value_accuracy_explanation=dsl.Field(),
        attribute_value_accuracy=dsl.Field(),
        entity_and_attribute_overview=dsl.Field(),
        attribute_measurement_frequency=dsl.Field(),
        entity_and_attribute_detail_citation=dsl.Field(),
        uniform_resource_identifier=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        display_note=dsl.Field(),
    ))

    @entity_and_attribute_information_note.creator('marc', '552..')
    @utils.for_each_value
    @utils.filter_values
    def entity_and_attribute_information_note(self, value):
        return {
            'entity_type_label': value.get('a'),
            'attribute_label': value.get('c'),
            'entity_type_definition_and_source': value.get('b'),
            'enumerated_domain_value': value.get('e'),
            'attribute_definition_and_source': value.get('d'),
            'range_domain_minimum_and_maximum': value.get('g'),
            'enumerated_domain_value_definition_and_source': value.get('f'),
            'unrepresentable_domain': value.get('i'),
            'codeset_name_and_source': value.get('h'),
            'beginning_and_ending_date_of_attribute_values': value.get('k'),
            'attribute_units_of_measurement_and_resolution': value.get('j'),
            'attribute_value_accuracy_explanation': value.get('m'),
            'attribute_value_accuracy': value.get('l'),
            'entity_and_attribute_overview': value.get('o'),
            'attribute_measurement_frequency': value.get('n'),
            'entity_and_attribute_detail_citation': value.get('p'),
            'uniform_resource_identifier': value.get('u'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'display_note': value.get('z')}

    cumulative_index_finding_aids_note = dsl.List(dsl.Object(
        cumulative_index_finding_aids_note=dsl.Field(),
        degree_of_control=dsl.Field(),
        availability_source=dsl.Field(),
        bibliographic_reference=dsl.Field(),
        materials_specified=dsl.Field(),
        uniform_resource_identifier=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @cumulative_index_finding_aids_note.creator('marc', '555..')
    @utils.for_each_value
    @utils.filter_values
    def cumulative_index_finding_aids_note(self, value):
        return {
            'cumulative_index_finding_aids_note': value.get('a'),
            'degree_of_control': value.get('c'),
            'availability_source': value.get('b'),
            'bibliographic_reference': value.get('d'),
            'materials_specified': value.get('3'),
            'uniform_resource_identifier': value.get('u'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    information_about_documentation_note = dsl.List(dsl.Object(
        information_about_documentation_note=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        international_standard_book_number=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @information_about_documentation_note.creator('marc', '556..')
    @utils.for_each_value
    @utils.filter_values
    def information_about_documentation_note(self, value):
        return {
            'information_about_documentation_note': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'international_standard_book_number': value.get('z'),
            'linkage': value.get('6')}

    ownership_and_custodial_history = dsl.List(dsl.Object(
        history=dsl.Field(),
        materials_specified=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        uniform_resource_identifier=dsl.Field(),
    ))

    @ownership_and_custodial_history.creator('marc', '561..')
    @utils.for_each_value
    @utils.filter_values
    def ownership_and_custodial_history(self, value):
        return {
            'history': value.get('a'),
            'materials_specified': value.get('3'),
            'institution_to_which_field_applies': value.get('5'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'uniform_resource_identifier': value.get('u')}

    copy_and_version_identification_note = dsl.List(dsl.Object(
        identifying_markings=dsl.Field(),
        version_identification=dsl.Field(),
        copy_identification=dsl.Field(),
        number_of_copies=dsl.Field(),
        presentation_format=dsl.Field(),
        materials_specified=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @copy_and_version_identification_note.creator('marc', '562..')
    @utils.for_each_value
    @utils.filter_values
    def copy_and_version_identification_note(self, value):
        return {
            'identifying_markings': value.get('a'),
            'version_identification': value.get('c'),
            'copy_identification': value.get('b'),
            'number_of_copies': value.get('e'),
            'presentation_format': value.get('d'),
            'materials_specified': value.get('3'),
            'institution_to_which_field_applies': value.get('5'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    binding_information = dsl.List(dsl.Object(
        binding_note=dsl.Field(),
        materials_specified=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        uniform_resource_identifier=dsl.Field(),
    ))

    @binding_information.creator('marc', '563..')
    @utils.for_each_value
    @utils.filter_values
    def binding_information(self, value):
        return {
            'binding_note': value.get('a'),
            'materials_specified': value.get('3'),
            'institution_to_which_field_applies': value.get('5'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'uniform_resource_identifier': value.get('u')}

    case_file_characteristics_note = dsl.List(dsl.Object(
        number_of_cases_variables=dsl.Field(),
        unit_of_analysis=dsl.Field(),
        name_of_variable=dsl.Field(),
        filing_scheme_or_code=dsl.Field(),
        universe_of_data=dsl.Field(),
        materials_specified=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @case_file_characteristics_note.creator('marc', '565..')
    @utils.for_each_value
    @utils.filter_values
    def case_file_characteristics_note(self, value):
        return {
            'number_of_cases_variables': value.get('a'),
            'unit_of_analysis': value.get('c'),
            'name_of_variable': value.get('b'),
            'filing_scheme_or_code': value.get('e'),
            'universe_of_data': value.get('d'),
            'materials_specified': value.get('3'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    methodology_note = dsl.List(dsl.Object(
        methodology_note=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @methodology_note.creator('marc', '567..')
    @utils.for_each_value
    @utils.filter_values
    def methodology_note(self, value):
        return {
            'methodology_note': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'linkage': value.get('6')}

    linking_entry_complexity_note = dsl.List(dsl.Object(
        linking_entry_complexity_note=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @linking_entry_complexity_note.creator('marc', '580..')
    @utils.for_each_value
    @utils.filter_values
    def linking_entry_complexity_note(self, value):
        return {
            'linking_entry_complexity_note': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'linkage': value.get('6')}

    publications_about_described_materials_note = dsl.List(dsl.Object(
        publications_about_described_materials_note=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        materials_specified=dsl.Field(),
        international_standard_book_number=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @publications_about_described_materials_note.creator('marc', '581..')
    @utils.for_each_value
    @utils.filter_values
    def publications_about_described_materials_note(self, value):
        return {
            'publications_about_described_materials_note': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'materials_specified': value.get('3'),
            'international_standard_book_number': value.get('z'),
            'linkage': value.get('6')}

    action_note = dsl.List(dsl.Object(
        action=dsl.Field(),
        nonpublic_note=dsl.Field(),
        time_date_of_action=dsl.Field(),
        action_identification=dsl.Field(),
        contingency_for_action=dsl.Field(),
        action_interval=dsl.Field(),
        authorization=dsl.Field(),
        method_of_action=dsl.Field(),
        jurisdiction=dsl.Field(),
        action_agent=dsl.Field(),
        site_of_action=dsl.Field(),
        status=dsl.Field(),
        type_of_unit=dsl.Field(),
        extent=dsl.Field(),
        materials_specified=dsl.Field(),
        source_of_term=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        public_note=dsl.Field(),
        uniform_resource_identifier=dsl.Field(),
    ))

    @action_note.creator('marc', '583..')
    @utils.for_each_value
    @utils.filter_values
    def action_note(self, value):
        return {
            'action': value.get('a'),
            'nonpublic_note': value.get('x'),
            'time_date_of_action': value.get('c'),
            'action_identification': value.get('b'),
            'contingency_for_action': value.get('e'),
            'action_interval': value.get('d'),
            'authorization': value.get('f'),
            'method_of_action': value.get('i'),
            'jurisdiction': value.get('h'),
            'action_agent': value.get('k'),
            'site_of_action': value.get('j'),
            'status': value.get('l'),
            'type_of_unit': value.get('o'),
            'extent': value.get('n'),
            'materials_specified': value.get('3'),
            'source_of_term': value.get('2'),
            'institution_to_which_field_applies': value.get('5'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'public_note': value.get('z'),
            'uniform_resource_identifier': value.get('u')}

    accumulation_and_frequency_of_use_note = dsl.List(dsl.Object(
        accumulation=dsl.Field(),
        frequency_of_use=dsl.Field(),
        materials_specified=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @accumulation_and_frequency_of_use_note.creator('marc', '584..')
    @utils.for_each_value
    @utils.filter_values
    def accumulation_and_frequency_of_use_note(self, value):
        return {
            'accumulation': value.get('a'),
            'frequency_of_use': value.get('b'),
            'materials_specified': value.get('3'),
            'institution_to_which_field_applies': value.get('5'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    exhibitions_note = dsl.List(dsl.Object(
        exhibitions_note=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        materials_specified=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @exhibitions_note.creator('marc', '585..')
    @utils.for_each_value
    @utils.filter_values
    def exhibitions_note(self, value):
        return {
            'exhibitions_note': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'materials_specified': value.get('3'),
            'institution_to_which_field_applies': value.get('5'),
            'linkage': value.get('6')}

    awards_note = dsl.List(dsl.Object(
        awards_note=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        materials_specified=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @awards_note.creator('marc', '586..')
    @utils.for_each_value
    @utils.filter_values
    def awards_note(self, value):
        return {
            'awards_note': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'materials_specified': value.get('3'),
            'linkage': value.get('6')}

    source_of_description_note = dsl.List(dsl.Object(
        source_of_description_note=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @source_of_description_note.creator('marc', '588..')
    @utils.for_each_value
    @utils.filter_values
    def source_of_description_note(self, value):
        return {
            'source_of_description_note': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'institution_to_which_field_applies': value.get('5'),
            'linkage': value.get('6')}

    subject_added_entry_personal_name = dsl.List(dsl.Object(
        authority_record_control_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source_of_heading_or_term=dsl.Field(),
        relator_code=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        personal_name=dsl.Field(),
        titles_and_other_words_associated_with_a_name=dsl.Field(),
        numeration=dsl.Field(),
        relator_term=dsl.Field(),
        dates_associated_with_a_name=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_of_a_work=dsl.Field(),
        medium=dsl.Field(),
        form_subheading=dsl.Field(),
        attribution_qualifier=dsl.Field(),
        medium_of_performance_for_music=dsl.Field(),
        language_of_a_work=dsl.Field(),
        arranged_statement_for_music=dsl.Field(),
        number_of_part_section_of_a_work=dsl.Field(),
        fuller_form_of_name=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        version=dsl.Field(),
        key_for_music=dsl.Field(),
        affiliation=dsl.Field(),
        title_of_a_work=dsl.Field(),
        form_subdivision=dsl.Field(),
        chronological_subdivision=dsl.Field(),
        general_subdivision=dsl.Field(),
        geographic_subdivision=dsl.Field(),
    ))

    @subject_added_entry_personal_name.creator('marc', '600..')
    @utils.for_each_value
    @utils.filter_values
    def subject_added_entry_personal_name(self, value):
        return {
            'authority_record_control_number': value.get('0'),
            'materials_specified': value.get('3'),
            'source_of_heading_or_term': value.get('2'),
            'relator_code': value.get('4'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'personal_name': value.get('a'),
            'titles_and_other_words_associated_with_a_name': value.get('c'),
            'numeration': value.get('b'),
            'relator_term': value.get('e'),
            'dates_associated_with_a_name': value.get('d'),
            'miscellaneous_information': value.get('g'),
            'date_of_a_work': value.get('f'),
            'medium': value.get('h'),
            'form_subheading': value.get('k'),
            'attribution_qualifier': value.get('j'),
            'medium_of_performance_for_music': value.get('m'),
            'language_of_a_work': value.get('l'),
            'arranged_statement_for_music': value.get('o'),
            'number_of_part_section_of_a_work': value.get('n'),
            'fuller_form_of_name': value.get('q'),
            'name_of_part_section_of_a_work': value.get('p'),
            'version': value.get('s'),
            'key_for_music': value.get('r'),
            'affiliation': value.get('u'),
            'title_of_a_work': value.get('t'),
            'form_subdivision': value.get('v'),
            'chronological_subdivision': value.get('y'),
            'general_subdivision': value.get('x'),
            'geographic_subdivision': value.get('z')}

    subject_added_entry_corporate_name = dsl.List(dsl.Object(
        authority_record_control_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source_of_heading_or_term=dsl.Field(),
        relator_code=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        corporate_name_or_jurisdiction_name_as_entry_element=dsl.Field(),
        location_of_meeting=dsl.Field(),
        subordinate_unit=dsl.Field(),
        relator_term=dsl.Field(),
        date_of_meeting_or_treaty_signing=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_of_a_work=dsl.Field(),
        medium=dsl.Field(),
        form_subheading=dsl.Field(),
        medium_of_performance_for_music=dsl.Field(),
        language_of_a_work=dsl.Field(),
        arranged_statement_for_music=dsl.Field(),
        number_of_part_section_meeting=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        version=dsl.Field(),
        key_for_music=dsl.Field(),
        affiliation=dsl.Field(),
        title_of_a_work=dsl.Field(),
        form_subdivision=dsl.Field(),
        chronological_subdivision=dsl.Field(),
        general_subdivision=dsl.Field(),
        geographic_subdivision=dsl.Field(),
    ))

    @subject_added_entry_corporate_name.creator('marc', '610..')
    @utils.for_each_value
    @utils.filter_values
    def subject_added_entry_corporate_name(self, value):
        return {
            'authority_record_control_number': value.get('0'),
            'materials_specified': value.get('3'),
            'source_of_heading_or_term': value.get('2'),
            'relator_code': value.get('4'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'corporate_name_or_jurisdiction_name_as_entry_element': value.get('a'),
            'location_of_meeting': value.get('c'),
            'subordinate_unit': value.get('b'),
            'relator_term': value.get('e'),
            'date_of_meeting_or_treaty_signing': value.get('d'),
            'miscellaneous_information': value.get('g'),
            'date_of_a_work': value.get('f'),
            'medium': value.get('h'),
            'form_subheading': value.get('k'),
            'medium_of_performance_for_music': value.get('m'),
            'language_of_a_work': value.get('l'),
            'arranged_statement_for_music': value.get('o'),
            'number_of_part_section_meeting': value.get('n'),
            'name_of_part_section_of_a_work': value.get('p'),
            'version': value.get('s'),
            'key_for_music': value.get('r'),
            'affiliation': value.get('u'),
            'title_of_a_work': value.get('t'),
            'form_subdivision': value.get('v'),
            'chronological_subdivision': value.get('y'),
            'general_subdivision': value.get('x'),
            'geographic_subdivision': value.get('z')}

    subject_added_entry_meeting_name = dsl.List(dsl.Object(
        authority_record_control_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source_of_heading_or_term=dsl.Field(),
        relator_code=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        meeting_name_or_jurisdiction_name_as_entry_element=dsl.Field(),
        location_of_meeting=dsl.Field(),
        subordinate_unit=dsl.Field(),
        date_of_meeting=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_of_a_work=dsl.Field(),
        medium=dsl.Field(),
        form_subheading=dsl.Field(),
        relator_term=dsl.Field(),
        language_of_a_work=dsl.Field(),
        number_of_part_section_meeting=dsl.Field(),
        name_of_meeting_following_jurisdiction_name_entry_element=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        version=dsl.Field(),
        affiliation=dsl.Field(),
        title_of_a_work=dsl.Field(),
        form_subdivision=dsl.Field(),
        chronological_subdivision=dsl.Field(),
        general_subdivision=dsl.Field(),
        geographic_subdivision=dsl.Field(),
    ))

    @subject_added_entry_meeting_name.creator('marc', '611..')
    @utils.for_each_value
    @utils.filter_values
    def subject_added_entry_meeting_name(self, value):
        return {
            'authority_record_control_number': value.get('0'),
            'materials_specified': value.get('3'),
            'source_of_heading_or_term': value.get('2'),
            'relator_code': value.get('4'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'meeting_name_or_jurisdiction_name_as_entry_element': value.get('a'),
            'location_of_meeting': value.get('c'),
            'subordinate_unit': value.get('e'),
            'date_of_meeting': value.get('d'),
            'miscellaneous_information': value.get('g'),
            'date_of_a_work': value.get('f'),
            'medium': value.get('h'),
            'form_subheading': value.get('k'),
            'relator_term': value.get('j'),
            'language_of_a_work': value.get('l'),
            'number_of_part_section_meeting': value.get('n'),
            'name_of_meeting_following_jurisdiction_name_entry_element': value.get('q'),
            'name_of_part_section_of_a_work': value.get('p'),
            'version': value.get('s'),
            'affiliation': value.get('u'),
            'title_of_a_work': value.get('t'),
            'form_subdivision': value.get('v'),
            'chronological_subdivision': value.get('y'),
            'general_subdivision': value.get('x'),
            'geographic_subdivision': value.get('z')}

    subject_added_entry_uniform_title = dsl.List(dsl.Object(
        authority_record_control_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source_of_heading_or_term=dsl.Field(),
        relator_code=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        uniform_title=dsl.Field(),
        relator_term=dsl.Field(),
        date_of_treaty_signing=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_of_a_work=dsl.Field(),
        medium=dsl.Field(),
        form_subheading=dsl.Field(),
        medium_of_performance_for_music=dsl.Field(),
        language_of_a_work=dsl.Field(),
        arranged_statement_for_music=dsl.Field(),
        number_of_part_section_of_a_work=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        version=dsl.Field(),
        key_for_music=dsl.Field(),
        title_of_a_work=dsl.Field(),
        form_subdivision=dsl.Field(),
        chronological_subdivision=dsl.Field(),
        general_subdivision=dsl.Field(),
        geographic_subdivision=dsl.Field(),
    ))

    @subject_added_entry_uniform_title.creator('marc', '630..')
    @utils.for_each_value
    @utils.filter_values
    def subject_added_entry_uniform_title(self, value):
        return {
            'authority_record_control_number': value.get('0'),
            'materials_specified': value.get('3'),
            'source_of_heading_or_term': value.get('2'),
            'relator_code': value.get('4'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'uniform_title': value.get('a'),
            'relator_term': value.get('e'),
            'date_of_treaty_signing': value.get('d'),
            'miscellaneous_information': value.get('g'),
            'date_of_a_work': value.get('f'),
            'medium': value.get('h'),
            'form_subheading': value.get('k'),
            'medium_of_performance_for_music': value.get('m'),
            'language_of_a_work': value.get('l'),
            'arranged_statement_for_music': value.get('o'),
            'number_of_part_section_of_a_work': value.get('n'),
            'name_of_part_section_of_a_work': value.get('p'),
            'version': value.get('s'),
            'key_for_music': value.get('r'),
            'title_of_a_work': value.get('t'),
            'form_subdivision': value.get('v'),
            'chronological_subdivision': value.get('y'),
            'general_subdivision': value.get('x'),
            'geographic_subdivision': value.get('z')}

    subject_added_entry_chronological_term = dsl.List(dsl.Object(
        chronological_term=dsl.Field(),
        general_subdivision=dsl.Field(),
        form_subdivision=dsl.Field(),
        authority_record_control_number_or_standard_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source_of_heading_or_term=dsl.Field(),
        linkage=dsl.Field(),
        chronological_subdivision=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        geographic_subdivision=dsl.Field(),
    ))

    @subject_added_entry_chronological_term.creator('marc', '648..')
    @utils.for_each_value
    @utils.filter_values
    def subject_added_entry_chronological_term(self, value):
        return {
            'chronological_term': value.get('a'),
            'general_subdivision': value.get('x'),
            'form_subdivision': value.get('v'),
            'authority_record_control_number_or_standard_number': value.get('0'),
            'materials_specified': value.get('3'),
            'source_of_heading_or_term': value.get('2'),
            'linkage': value.get('6'),
            'chronological_subdivision': value.get('y'),
            'field_link_and_sequence_number': value.get('8'),
            'geographic_subdivision': value.get('z')}

    subject_added_entry_topical_term = dsl.List(dsl.Object(
        topical_term_or_geographic_name_entry_element=dsl.Field(),
        general_subdivision=dsl.Field(),
        location_of_event=dsl.Field(),
        topical_term_following_geographic_name_entry_element=dsl.Field(),
        relator_term=dsl.Field(),
        active_dates=dsl.Field(),
        form_subdivision=dsl.Field(),
        authority_record_control_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source_of_heading_or_term=dsl.Field(),
        relator_code=dsl.Field(),
        linkage=dsl.Field(),
        chronological_subdivision=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        geographic_subdivision=dsl.Field(),
    ))

    @subject_added_entry_topical_term.creator('marc', '650..')
    @utils.for_each_value
    @utils.filter_values
    def subject_added_entry_topical_term(self, value):
        return {
            'topical_term_or_geographic_name_entry_element': value.get('a'),
            'general_subdivision': value.get('x'),
            'location_of_event': value.get('c'),
            'topical_term_following_geographic_name_entry_element': value.get('b'),
            'relator_term': value.get('e'),
            'active_dates': value.get('d'),
            'form_subdivision': value.get('v'),
            'authority_record_control_number': value.get('0'),
            'materials_specified': value.get('3'),
            'source_of_heading_or_term': value.get('2'),
            'relator_code': value.get('4'),
            'linkage': value.get('6'),
            'chronological_subdivision': value.get('y'),
            'field_link_and_sequence_number': value.get('8'),
            'geographic_subdivision': value.get('z')}

    subject_added_entry_geographic_name = dsl.List(dsl.Object(
        geographic_name=dsl.Field(),
        general_subdivision=dsl.Field(),
        relator_term=dsl.Field(),
        form_subdivision=dsl.Field(),
        authority_record_control_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source_of_heading_or_term=dsl.Field(),
        relator_code=dsl.Field(),
        linkage=dsl.Field(),
        chronological_subdivision=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        geographic_subdivision=dsl.Field(),
    ))

    @subject_added_entry_geographic_name.creator('marc', '651..')
    @utils.for_each_value
    @utils.filter_values
    def subject_added_entry_geographic_name(self, value):
        return {
            'geographic_name': value.get('a'),
            'general_subdivision': value.get('x'),
            'relator_term': value.get('e'),
            'form_subdivision': value.get('v'),
            'authority_record_control_number': value.get('0'),
            'materials_specified': value.get('3'),
            'source_of_heading_or_term': value.get('2'),
            'relator_code': value.get('4'),
            'linkage': value.get('6'),
            'chronological_subdivision': value.get('y'),
            'field_link_and_sequence_number': value.get('8'),
            'geographic_subdivision': value.get('z')}

    index_term_uncontrolled = dsl.List(dsl.Object(
        uncontrolled_term=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @index_term_uncontrolled.creator('marc', '653..')
    @utils.for_each_value
    @utils.filter_values
    def index_term_uncontrolled(self, value):
        return {
            'uncontrolled_term': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'linkage': value.get('6')}

    subject_added_entry_faceted_topical_terms = dsl.List(dsl.Object(
        focus_term=dsl.Field(),
        facet_hierarchy_designation=dsl.Field(),
        non_focus_term=dsl.Field(),
        relator_term=dsl.Field(),
        form_subdivision=dsl.Field(),
        authority_record_control_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source_of_heading_or_term=dsl.Field(),
        relator_code=dsl.Field(),
        linkage=dsl.Field(),
        chronological_subdivision=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        geographic_subdivision=dsl.Field(),
    ))

    @subject_added_entry_faceted_topical_terms.creator('marc', '654..')
    @utils.for_each_value
    @utils.filter_values
    def subject_added_entry_faceted_topical_terms(self, value):
        return {
            'focus_term': value.get('a'),
            'facet_hierarchy_designation': value.get('c'),
            'non_focus_term': value.get('b'),
            'relator_term': value.get('e'),
            'form_subdivision': value.get('v'),
            'authority_record_control_number': value.get('0'),
            'materials_specified': value.get('3'),
            'source_of_heading_or_term': value.get('2'),
            'relator_code': value.get('4'),
            'linkage': value.get('6'),
            'chronological_subdivision': value.get('y'),
            'field_link_and_sequence_number': value.get('8'),
            'geographic_subdivision': value.get('z')}

    index_term_genre_form = dsl.List(dsl.Object(
        genre_form_data_or_focus_term=dsl.Field(),
        general_subdivision=dsl.Field(),
        facet_hierarchy_designation=dsl.Field(),
        non_focus_term=dsl.Field(),
        form_subdivision=dsl.Field(),
        authority_record_control_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source_of_term=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        linkage=dsl.Field(),
        chronological_subdivision=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        geographic_subdivision=dsl.Field(),
    ))

    @index_term_genre_form.creator('marc', '655..')
    @utils.for_each_value
    @utils.filter_values
    def index_term_genre_form(self, value):
        return {
            'genre_form_data_or_focus_term': value.get('a'),
            'general_subdivision': value.get('x'),
            'facet_hierarchy_designation': value.get('c'),
            'non_focus_term': value.get('b'),
            'form_subdivision': value.get('v'),
            'authority_record_control_number': value.get('0'),
            'materials_specified': value.get('3'),
            'source_of_term': value.get('2'),
            'institution_to_which_field_applies': value.get('5'),
            'linkage': value.get('6'),
            'chronological_subdivision': value.get('y'),
            'field_link_and_sequence_number': value.get('8'),
            'geographic_subdivision': value.get('z')}

    index_term_occupation = dsl.List(dsl.Object(
        occupation=dsl.Field(),
        general_subdivision=dsl.Field(),
        form=dsl.Field(),
        form_subdivision=dsl.Field(),
        authority_record_control_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source_of_term=dsl.Field(),
        linkage=dsl.Field(),
        chronological_subdivision=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        geographic_subdivision=dsl.Field(),
    ))

    @index_term_occupation.creator('marc', '656..')
    @utils.for_each_value
    @utils.filter_values
    def index_term_occupation(self, value):
        return {
            'occupation': value.get('a'),
            'general_subdivision': value.get('x'),
            'form': value.get('k'),
            'form_subdivision': value.get('v'),
            'authority_record_control_number': value.get('0'),
            'materials_specified': value.get('3'),
            'source_of_term': value.get('2'),
            'linkage': value.get('6'),
            'chronological_subdivision': value.get('y'),
            'field_link_and_sequence_number': value.get('8'),
            'geographic_subdivision': value.get('z')}

    index_term_function = dsl.List(dsl.Object(
        function=dsl.Field(),
        general_subdivision=dsl.Field(),
        form_subdivision=dsl.Field(),
        authority_record_control_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source_of_term=dsl.Field(),
        linkage=dsl.Field(),
        chronological_subdivision=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        geographic_subdivision=dsl.Field(),
    ))

    @index_term_function.creator('marc', '657..')
    @utils.for_each_value
    @utils.filter_values
    def index_term_function(self, value):
        return {
            'function': value.get('a'),
            'general_subdivision': value.get('x'),
            'form_subdivision': value.get('v'),
            'authority_record_control_number': value.get('0'),
            'materials_specified': value.get('3'),
            'source_of_term': value.get('2'),
            'linkage': value.get('6'),
            'chronological_subdivision': value.get('y'),
            'field_link_and_sequence_number': value.get('8'),
            'geographic_subdivision': value.get('z')}

    index_term_curriculum_objective = dsl.List(dsl.Object(
        main_curriculum_objective=dsl.Field(),
        curriculum_code=dsl.Field(),
        subordinate_curriculum_objective=dsl.Field(),
        correlation_factor=dsl.Field(),
        source_of_term_or_code=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @index_term_curriculum_objective.creator('marc', '658..')
    @utils.for_each_value
    @utils.filter_values
    def index_term_curriculum_objective(self, value):
        return {
            'main_curriculum_objective': value.get('a'),
            'curriculum_code': value.get('c'),
            'subordinate_curriculum_objective': value.get('b'),
            'correlation_factor': value.get('d'),
            'source_of_term_or_code': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    subject_added_entry_hierarchical_place_name = dsl.List(dsl.Object(
        country_or_larger_entity=dsl.Field(),
        intermediate_political_jurisdiction=dsl.Field(),
        first_order_political_jurisdiction=dsl.Field(),
        relator_term=dsl.Field(),
        city=dsl.Field(),
        other_nonjurisdictional_geographic_region_and_feature=dsl.Field(),
        city_subsection=dsl.Field(),
        extraterrestrial_area=dsl.Field(),
        authority_record_control_number=dsl.Field(),
        source_of_heading_or_term=dsl.Field(),
        relator_code=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @subject_added_entry_hierarchical_place_name.creator('marc', '662..')
    @utils.for_each_value
    @utils.filter_values
    def subject_added_entry_hierarchical_place_name(self, value):
        return {
            'country_or_larger_entity': value.get('a'),
            'intermediate_political_jurisdiction': value.get('c'),
            'first_order_political_jurisdiction': value.get('b'),
            'relator_term': value.get('e'),
            'city': value.get('d'),
            'other_nonjurisdictional_geographic_region_and_feature': value.get('g'),
            'city_subsection': value.get('f'),
            'extraterrestrial_area': value.get('h'),
            'authority_record_control_number': value.get('0'),
            'source_of_heading_or_term': value.get('2'),
            'relator_code': value.get('4'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    added_entry_personal_name = dsl.List(dsl.Object(
        authority_record_control_number=dsl.Field(),
        materials_specified=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        relator_code=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        personal_name=dsl.Field(),
        titles_and_other_words_associated_with_a_name=dsl.Field(),
        numeration=dsl.Field(),
        relator_term=dsl.Field(),
        dates_associated_with_a_name=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_of_a_work=dsl.Field(),
        relationship_information=dsl.Field(),
        medium=dsl.Field(),
        form_subheading=dsl.Field(),
        attribution_qualifier=dsl.Field(),
        medium_of_performance_for_music=dsl.Field(),
        language_of_a_work=dsl.Field(),
        arranged_statement_for_music=dsl.Field(),
        number_of_part_section_of_a_work=dsl.Field(),
        fuller_form_of_name=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        version=dsl.Field(),
        key_for_music=dsl.Field(),
        affiliation=dsl.Field(),
        title_of_a_work=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
    ))

    @added_entry_personal_name.creator('marc', '700..')
    @utils.for_each_value
    @utils.filter_values
    def added_entry_personal_name(self, value):
        return {
            'authority_record_control_number': value.get('0'),
            'materials_specified': value.get('3'),
            'institution_to_which_field_applies': value.get('5'),
            'relator_code': value.get('4'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'personal_name': value.get('a'),
            'titles_and_other_words_associated_with_a_name': value.get('c'),
            'numeration': value.get('b'),
            'relator_term': value.get('e'),
            'dates_associated_with_a_name': value.get('d'),
            'miscellaneous_information': value.get('g'),
            'date_of_a_work': value.get('f'),
            'relationship_information': value.get('i'),
            'medium': value.get('h'),
            'form_subheading': value.get('k'),
            'attribution_qualifier': value.get('j'),
            'medium_of_performance_for_music': value.get('m'),
            'language_of_a_work': value.get('l'),
            'arranged_statement_for_music': value.get('o'),
            'number_of_part_section_of_a_work': value.get('n'),
            'fuller_form_of_name': value.get('q'),
            'name_of_part_section_of_a_work': value.get('p'),
            'version': value.get('s'),
            'key_for_music': value.get('r'),
            'affiliation': value.get('u'),
            'title_of_a_work': value.get('t'),
            'international_standard_serial_number': value.get('x')}

    added_entry_corporate_name = dsl.List(dsl.Object(
        authority_record_control_number=dsl.Field(),
        materials_specified=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        relator_code=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        corporate_name_or_jurisdiction_name_as_entry_element=dsl.Field(),
        location_of_meeting=dsl.Field(),
        subordinate_unit=dsl.Field(),
        relator_term=dsl.Field(),
        date_of_meeting_or_treaty_signing=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_of_a_work=dsl.Field(),
        relationship_information=dsl.Field(),
        medium=dsl.Field(),
        form_subheading=dsl.Field(),
        medium_of_performance_for_music=dsl.Field(),
        language_of_a_work=dsl.Field(),
        arranged_statement_for_music=dsl.Field(),
        number_of_part_section_meeting=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        version=dsl.Field(),
        key_for_music=dsl.Field(),
        affiliation=dsl.Field(),
        title_of_a_work=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
    ))

    @added_entry_corporate_name.creator('marc', '710..')
    @utils.for_each_value
    @utils.filter_values
    def added_entry_corporate_name(self, value):
        return {
            'authority_record_control_number': value.get('0'),
            'materials_specified': value.get('3'),
            'institution_to_which_field_applies': value.get('5'),
            'relator_code': value.get('4'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'corporate_name_or_jurisdiction_name_as_entry_element': value.get('a'),
            'location_of_meeting': value.get('c'),
            'subordinate_unit': value.get('b'),
            'relator_term': value.get('e'),
            'date_of_meeting_or_treaty_signing': value.get('d'),
            'miscellaneous_information': value.get('g'),
            'date_of_a_work': value.get('f'),
            'relationship_information': value.get('i'),
            'medium': value.get('h'),
            'form_subheading': value.get('k'),
            'medium_of_performance_for_music': value.get('m'),
            'language_of_a_work': value.get('l'),
            'arranged_statement_for_music': value.get('o'),
            'number_of_part_section_meeting': value.get('n'),
            'name_of_part_section_of_a_work': value.get('p'),
            'version': value.get('s'),
            'key_for_music': value.get('r'),
            'affiliation': value.get('u'),
            'title_of_a_work': value.get('t'),
            'international_standard_serial_number': value.get('x')}

    added_entry_meeting_name = dsl.List(dsl.Object(
        authority_record_control_number=dsl.Field(),
        materials_specified=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        relator_code=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        meeting_name_or_jurisdiction_name_as_entry_element=dsl.Field(),
        location_of_meeting=dsl.Field(),
        subordinate_unit=dsl.Field(),
        date_of_meeting=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_of_a_work=dsl.Field(),
        relationship_information=dsl.Field(),
        medium=dsl.Field(),
        form_subheading=dsl.Field(),
        relator_term=dsl.Field(),
        language_of_a_work=dsl.Field(),
        number_of_part_section_meeting=dsl.Field(),
        name_of_meeting_following_jurisdiction_name_entry_element=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        version=dsl.Field(),
        affiliation=dsl.Field(),
        title_of_a_work=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
    ))

    @added_entry_meeting_name.creator('marc', '711..')
    @utils.for_each_value
    @utils.filter_values
    def added_entry_meeting_name(self, value):
        return {
            'authority_record_control_number': value.get('0'),
            'materials_specified': value.get('3'),
            'institution_to_which_field_applies': value.get('5'),
            'relator_code': value.get('4'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'meeting_name_or_jurisdiction_name_as_entry_element': value.get('a'),
            'location_of_meeting': value.get('c'),
            'subordinate_unit': value.get('e'),
            'date_of_meeting': value.get('d'),
            'miscellaneous_information': value.get('g'),
            'date_of_a_work': value.get('f'),
            'relationship_information': value.get('i'),
            'medium': value.get('h'),
            'form_subheading': value.get('k'),
            'relator_term': value.get('j'),
            'language_of_a_work': value.get('l'),
            'number_of_part_section_meeting': value.get('n'),
            'name_of_meeting_following_jurisdiction_name_entry_element': value.get('q'),
            'name_of_part_section_of_a_work': value.get('p'),
            'version': value.get('s'),
            'affiliation': value.get('u'),
            'title_of_a_work': value.get('t'),
            'international_standard_serial_number': value.get('x')}

    added_entry_uncontrolled_name = dsl.List(dsl.Object(
        name=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        relator_term=dsl.Field(),
        relator_code=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @added_entry_uncontrolled_name.creator('marc', '720..')
    @utils.for_each_value
    @utils.filter_values
    def added_entry_uncontrolled_name(self, value):
        return {
            'name': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'relator_term': value.get('e'),
            'relator_code': value.get('4'),
            'linkage': value.get('6')}

    added_entry_uniform_title = dsl.List(dsl.Object(
        uniform_title=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        date_of_treaty_signing=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_of_a_work=dsl.Field(),
        relationship_information=dsl.Field(),
        medium=dsl.Field(),
        form_subheading=dsl.Field(),
        medium_of_performance_for_music=dsl.Field(),
        language_of_a_work=dsl.Field(),
        arranged_statement_for_music=dsl.Field(),
        number_of_part_section_of_a_work=dsl.Field(),
        authority_record_control_number=dsl.Field(),
        materials_specified=dsl.Field(),
        key_for_music=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        title_of_a_work=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        version=dsl.Field(),
    ))

    @added_entry_uniform_title.creator('marc', '730..')
    @utils.for_each_value
    @utils.filter_values
    def added_entry_uniform_title(self, value):
        return {
            'uniform_title': value.get('a'),
            'international_standard_serial_number': value.get('x'),
            'name_of_part_section_of_a_work': value.get('p'),
            'date_of_treaty_signing': value.get('d'),
            'miscellaneous_information': value.get('g'),
            'date_of_a_work': value.get('f'),
            'relationship_information': value.get('i'),
            'medium': value.get('h'),
            'form_subheading': value.get('k'),
            'medium_of_performance_for_music': value.get('m'),
            'language_of_a_work': value.get('l'),
            'arranged_statement_for_music': value.get('o'),
            'number_of_part_section_of_a_work': value.get('n'),
            'authority_record_control_number': value.get('0'),
            'materials_specified': value.get('3'),
            'key_for_music': value.get('r'),
            'institution_to_which_field_applies': value.get('5'),
            'title_of_a_work': value.get('t'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'version': value.get('s')}

    added_entry_uncontrolled_related_analytical_title = dsl.List(dsl.Object(
        uncontrolled_related_analytical_title=dsl.Field(),
        medium=dsl.Field(),
        number_of_part_section_of_a_work=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @added_entry_uncontrolled_related_analytical_title.creator('marc', '740..')
    @utils.for_each_value
    @utils.filter_values
    def added_entry_uncontrolled_related_analytical_title(self, value):
        return {
            'uncontrolled_related_analytical_title': value.get('a'),
            'medium': value.get('h'),
            'number_of_part_section_of_a_work': value.get('n'),
            'name_of_part_section_of_a_work': value.get('p'),
            'institution_to_which_field_applies': value.get('5'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    added_entry_geographic_name = dsl.List(dsl.Object(
        geographic_name=dsl.Field(),
        relator_term=dsl.Field(),
        authority_record_control_number=dsl.Field(),
        materials_specified=dsl.Field(),
        source_of_heading_or_term=dsl.Field(),
        relator_code=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @added_entry_geographic_name.creator('marc', '751..')
    @utils.for_each_value
    @utils.filter_values
    def added_entry_geographic_name(self, value):
        return {
            'geographic_name': value.get('a'),
            'relator_term': value.get('e'),
            'authority_record_control_number': value.get('0'),
            'materials_specified': value.get('3'),
            'source_of_heading_or_term': value.get('2'),
            'relator_code': value.get('4'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    added_entry_hierarchical_place_name = dsl.List(dsl.Object(
        country_or_larger_entity=dsl.Field(),
        intermediate_political_jurisdiction=dsl.Field(),
        first_order_political_jurisdiction=dsl.Field(),
        city=dsl.Field(),
        other_nonjurisdictional_geographic_region_and_feature=dsl.Field(),
        city_subsection=dsl.Field(),
        extraterrestrial_area=dsl.Field(),
        authority_record_control_number=dsl.Field(),
        source_of_heading_or_term=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @added_entry_hierarchical_place_name.creator('marc', '752..')
    @utils.for_each_value
    @utils.filter_values
    def added_entry_hierarchical_place_name(self, value):
        return {
            'country_or_larger_entity': value.get('a'),
            'intermediate_political_jurisdiction': value.get('c'),
            'first_order_political_jurisdiction': value.get('b'),
            'city': value.get('d'),
            'other_nonjurisdictional_geographic_region_and_feature': value.get('g'),
            'city_subsection': value.get('f'),
            'extraterrestrial_area': value.get('h'),
            'authority_record_control_number': value.get('0'),
            'source_of_heading_or_term': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8')}

    system_details_access_to_computer_files = dsl.List(dsl.Object(
        make_and_model_of_machine=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        operating_system=dsl.Field(),
        programming_language=dsl.Field(),
        linkage=dsl.Field(),
    ))

    @system_details_access_to_computer_files.creator('marc', '753..')
    @utils.for_each_value
    @utils.filter_values
    def system_details_access_to_computer_files(self, value):
        return {
            'make_and_model_of_machine': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'operating_system': value.get('c'),
            'programming_language': value.get('b'),
            'linkage': value.get('6')}

    added_entry_taxonomic_identification = dsl.List(dsl.Object(
        taxonomic_name=dsl.Field(),
        non_public_note=dsl.Field(),
        taxonomic_category=dsl.Field(),
        common_or_alternative_name=dsl.Field(),
        authority_record_control_number=dsl.Field(),
        source_of_taxonomic_identification=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        public_note=dsl.Field(),
    ))

    @added_entry_taxonomic_identification.creator('marc', '754..')
    @utils.for_each_value
    @utils.filter_values
    def added_entry_taxonomic_identification(self, value):
        return {
            'taxonomic_name': value.get('a'),
            'non_public_note': value.get('x'),
            'taxonomic_category': value.get('c'),
            'common_or_alternative_name': value.get('d'),
            'authority_record_control_number': value.get('0'),
            'source_of_taxonomic_identification': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'public_note': value.get('z')}

    main_series_entry = dsl.List(dsl.Object(
        main_entry_heading=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        qualifying_information=dsl.Field(),
        edition=dsl.Field(),
        place_publisher_and_date_of_publication=dsl.Field(),
        related_parts=dsl.Field(),
        relationship_information=dsl.Field(),
        physical_description=dsl.Field(),
        material_specific_details=dsl.Field(),
        other_item_identifier=dsl.Field(),
        note=dsl.Field(),
        record_control_number=dsl.Field(),
        uniform_title=dsl.Field(),
        relationship_code=dsl.Field(),
        control_subfield=dsl.Field(),
        linkage=dsl.Field(),
        coden_designation=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        title=dsl.Field(),
    ))

    @main_series_entry.creator('marc', '760..')
    @utils.for_each_value
    @utils.filter_values
    def main_series_entry(self, value):
        return {
            'main_entry_heading': value.get('a'),
            'international_standard_serial_number': value.get('x'),
            'qualifying_information': value.get('c'),
            'edition': value.get('b'),
            'place_publisher_and_date_of_publication': value.get('d'),
            'related_parts': value.get('g'),
            'relationship_information': value.get('i'),
            'physical_description': value.get('h'),
            'material_specific_details': value.get('m'),
            'other_item_identifier': value.get('o'),
            'note': value.get('n'),
            'record_control_number': value.get('w'),
            'uniform_title': value.get('s'),
            'relationship_code': value.get('4'),
            'control_subfield': value.get('7'),
            'linkage': value.get('6'),
            'coden_designation': value.get('y'),
            'field_link_and_sequence_number': value.get('8'),
            'title': value.get('t')}

    subseries_entry = dsl.List(dsl.Object(
        main_entry_heading=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        qualifying_information=dsl.Field(),
        edition=dsl.Field(),
        place_publisher_and_date_of_publication=dsl.Field(),
        related_parts=dsl.Field(),
        relationship_information=dsl.Field(),
        physical_description=dsl.Field(),
        material_specific_details=dsl.Field(),
        other_item_identifier=dsl.Field(),
        note=dsl.Field(),
        record_control_number=dsl.Field(),
        uniform_title=dsl.Field(),
        relationship_code=dsl.Field(),
        control_subfield=dsl.Field(),
        linkage=dsl.Field(),
        coden_designation=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        title=dsl.Field(),
    ))

    @subseries_entry.creator('marc', '762..')
    @utils.for_each_value
    @utils.filter_values
    def subseries_entry(self, value):
        return {
            'main_entry_heading': value.get('a'),
            'international_standard_serial_number': value.get('x'),
            'qualifying_information': value.get('c'),
            'edition': value.get('b'),
            'place_publisher_and_date_of_publication': value.get('d'),
            'related_parts': value.get('g'),
            'relationship_information': value.get('i'),
            'physical_description': value.get('h'),
            'material_specific_details': value.get('m'),
            'other_item_identifier': value.get('o'),
            'note': value.get('n'),
            'record_control_number': value.get('w'),
            'uniform_title': value.get('s'),
            'relationship_code': value.get('4'),
            'control_subfield': value.get('7'),
            'linkage': value.get('6'),
            'coden_designation': value.get('y'),
            'field_link_and_sequence_number': value.get('8'),
            'title': value.get('t')}

    original_language_entry = dsl.List(dsl.Object(
        relationship_code=dsl.Field(),
        control_subfield=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        main_entry_heading=dsl.Field(),
        qualifying_information=dsl.Field(),
        edition=dsl.Field(),
        place_publisher_and_date_of_publication=dsl.Field(),
        related_parts=dsl.Field(),
        relationship_information=dsl.Field(),
        physical_description=dsl.Field(),
        series_data_for_related_item=dsl.Field(),
        material_specific_details=dsl.Field(),
        other_item_identifier=dsl.Field(),
        note=dsl.Field(),
        uniform_title=dsl.Field(),
        report_number=dsl.Field(),
        standard_technical_report_number=dsl.Field(),
        title=dsl.Field(),
        record_control_number=dsl.Field(),
        coden_designation=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        international_standard_book_number=dsl.Field(),
    ))

    @original_language_entry.creator('marc', '765..')
    @utils.for_each_value
    @utils.filter_values
    def original_language_entry(self, value):
        return {
            'relationship_code': value.get('4'),
            'control_subfield': value.get('7'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'main_entry_heading': value.get('a'),
            'qualifying_information': value.get('c'),
            'edition': value.get('b'),
            'place_publisher_and_date_of_publication': value.get('d'),
            'related_parts': value.get('g'),
            'relationship_information': value.get('i'),
            'physical_description': value.get('h'),
            'series_data_for_related_item': value.get('k'),
            'material_specific_details': value.get('m'),
            'other_item_identifier': value.get('o'),
            'note': value.get('n'),
            'uniform_title': value.get('s'),
            'report_number': value.get('r'),
            'standard_technical_report_number': value.get('u'),
            'title': value.get('t'),
            'record_control_number': value.get('w'),
            'coden_designation': value.get('y'),
            'international_standard_serial_number': value.get('x'),
            'international_standard_book_number': value.get('z')}

    translation_entry = dsl.List(dsl.Object(
        relationship_code=dsl.Field(),
        control_subfield=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        main_entry_heading=dsl.Field(),
        qualifying_information=dsl.Field(),
        edition=dsl.Field(),
        place_publisher_and_date_of_publication=dsl.Field(),
        related_parts=dsl.Field(),
        relationship_information=dsl.Field(),
        physical_description=dsl.Field(),
        series_data_for_related_item=dsl.Field(),
        material_specific_details=dsl.Field(),
        other_item_identifier=dsl.Field(),
        note=dsl.Field(),
        uniform_title=dsl.Field(),
        report_number=dsl.Field(),
        standard_technical_report_number=dsl.Field(),
        title=dsl.Field(),
        record_control_number=dsl.Field(),
        coden_designation=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        international_standard_book_number=dsl.Field(),
    ))

    @translation_entry.creator('marc', '767..')
    @utils.for_each_value
    @utils.filter_values
    def translation_entry(self, value):
        return {
            'relationship_code': value.get('4'),
            'control_subfield': value.get('7'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'main_entry_heading': value.get('a'),
            'qualifying_information': value.get('c'),
            'edition': value.get('b'),
            'place_publisher_and_date_of_publication': value.get('d'),
            'related_parts': value.get('g'),
            'relationship_information': value.get('i'),
            'physical_description': value.get('h'),
            'series_data_for_related_item': value.get('k'),
            'material_specific_details': value.get('m'),
            'other_item_identifier': value.get('o'),
            'note': value.get('n'),
            'uniform_title': value.get('s'),
            'report_number': value.get('r'),
            'standard_technical_report_number': value.get('u'),
            'title': value.get('t'),
            'record_control_number': value.get('w'),
            'coden_designation': value.get('y'),
            'international_standard_serial_number': value.get('x'),
            'international_standard_book_number': value.get('z')}

    supplement_special_issue_entry = dsl.List(dsl.Object(
        relationship_code=dsl.Field(),
        control_subfield=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        main_entry_heading=dsl.Field(),
        qualifying_information=dsl.Field(),
        edition=dsl.Field(),
        place_publisher_and_date_of_publication=dsl.Field(),
        related_parts=dsl.Field(),
        relationship_information=dsl.Field(),
        physical_description=dsl.Field(),
        series_data_for_related_item=dsl.Field(),
        material_specific_details=dsl.Field(),
        other_item_identifier=dsl.Field(),
        note=dsl.Field(),
        uniform_title=dsl.Field(),
        report_number=dsl.Field(),
        standard_technical_report_number=dsl.Field(),
        title=dsl.Field(),
        record_control_number=dsl.Field(),
        coden_designation=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        international_standard_book_number=dsl.Field(),
    ))

    @supplement_special_issue_entry.creator('marc', '770..')
    @utils.for_each_value
    @utils.filter_values
    def supplement_special_issue_entry(self, value):
        return {
            'relationship_code': value.get('4'),
            'control_subfield': value.get('7'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'main_entry_heading': value.get('a'),
            'qualifying_information': value.get('c'),
            'edition': value.get('b'),
            'place_publisher_and_date_of_publication': value.get('d'),
            'related_parts': value.get('g'),
            'relationship_information': value.get('i'),
            'physical_description': value.get('h'),
            'series_data_for_related_item': value.get('k'),
            'material_specific_details': value.get('m'),
            'other_item_identifier': value.get('o'),
            'note': value.get('n'),
            'uniform_title': value.get('s'),
            'report_number': value.get('r'),
            'standard_technical_report_number': value.get('u'),
            'title': value.get('t'),
            'record_control_number': value.get('w'),
            'coden_designation': value.get('y'),
            'international_standard_serial_number': value.get('x'),
            'international_standard_book_number': value.get('z')}

    supplement_parent_entry = dsl.List(dsl.Object(
        relationship_code=dsl.Field(),
        control_subfield=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        main_entry_heading=dsl.Field(),
        qualifying_information=dsl.Field(),
        edition=dsl.Field(),
        place_publisher_and_date_of_publication=dsl.Field(),
        related_parts=dsl.Field(),
        relationship_information=dsl.Field(),
        physical_description=dsl.Field(),
        series_data_for_related_item=dsl.Field(),
        material_specific_details=dsl.Field(),
        other_item_identifier=dsl.Field(),
        note=dsl.Field(),
        uniform_title=dsl.Field(),
        report_number=dsl.Field(),
        standard_technical_report_number=dsl.Field(),
        title=dsl.Field(),
        record_control_number=dsl.Field(),
        coden_designation=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        international_standard_book_number=dsl.Field(),
    ))

    @supplement_parent_entry.creator('marc', '772..')
    @utils.for_each_value
    @utils.filter_values
    def supplement_parent_entry(self, value):
        return {
            'relationship_code': value.get('4'),
            'control_subfield': value.get('7'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'main_entry_heading': value.get('a'),
            'qualifying_information': value.get('c'),
            'edition': value.get('b'),
            'place_publisher_and_date_of_publication': value.get('d'),
            'related_parts': value.get('g'),
            'relationship_information': value.get('i'),
            'physical_description': value.get('h'),
            'series_data_for_related_item': value.get('k'),
            'material_specific_details': value.get('m'),
            'other_item_identifier': value.get('o'),
            'note': value.get('n'),
            'uniform_title': value.get('s'),
            'report_number': value.get('r'),
            'standard_technical_report_number': value.get('u'),
            'title': value.get('t'),
            'record_control_number': value.get('w'),
            'coden_designation': value.get('y'),
            'international_standard_serial_number': value.get('x'),
            'international_standard_book_number': value.get('z')}

    host_item_entry = dsl.List(dsl.Object(
        materials_specified=dsl.Field(),
        relationship_code=dsl.Field(),
        control_subfield=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        main_entry_heading=dsl.Field(),
        edition=dsl.Field(),
        place_publisher_and_date_of_publication=dsl.Field(),
        related_parts=dsl.Field(),
        relationship_information=dsl.Field(),
        physical_description=dsl.Field(),
        series_data_for_related_item=dsl.Field(),
        material_specific_details=dsl.Field(),
        other_item_identifier=dsl.Field(),
        note=dsl.Field(),
        enumeration_and_first_page=dsl.Field(),
        abbreviated_title=dsl.Field(),
        uniform_title=dsl.Field(),
        report_number=dsl.Field(),
        standard_technical_report_number=dsl.Field(),
        title=dsl.Field(),
        record_control_number=dsl.Field(),
        coden_designation=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        international_standard_book_number=dsl.Field(),
    ))

    @host_item_entry.creator('marc', '773..')
    @utils.for_each_value
    @utils.filter_values
    def host_item_entry(self, value):
        return {
            'materials_specified': value.get('3'),
            'relationship_code': value.get('4'),
            'control_subfield': value.get('7'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'main_entry_heading': value.get('a'),
            'edition': value.get('b'),
            'place_publisher_and_date_of_publication': value.get('d'),
            'related_parts': value.get('g'),
            'relationship_information': value.get('i'),
            'physical_description': value.get('h'),
            'series_data_for_related_item': value.get('k'),
            'material_specific_details': value.get('m'),
            'other_item_identifier': value.get('o'),
            'note': value.get('n'),
            'enumeration_and_first_page': value.get('q'),
            'abbreviated_title': value.get('p'),
            'uniform_title': value.get('s'),
            'report_number': value.get('r'),
            'standard_technical_report_number': value.get('u'),
            'title': value.get('t'),
            'record_control_number': value.get('w'),
            'coden_designation': value.get('y'),
            'international_standard_serial_number': value.get('x'),
            'international_standard_book_number': value.get('z')}

    constituent_unit_entry = dsl.List(dsl.Object(
        relationship_code=dsl.Field(),
        control_subfield=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        main_entry_heading=dsl.Field(),
        qualifying_information=dsl.Field(),
        edition=dsl.Field(),
        place_publisher_and_date_of_publication=dsl.Field(),
        related_parts=dsl.Field(),
        relationship_information=dsl.Field(),
        physical_description=dsl.Field(),
        series_data_for_related_item=dsl.Field(),
        material_specific_details=dsl.Field(),
        other_item_identifier=dsl.Field(),
        note=dsl.Field(),
        uniform_title=dsl.Field(),
        report_number=dsl.Field(),
        standard_technical_report_number=dsl.Field(),
        title=dsl.Field(),
        record_control_number=dsl.Field(),
        coden_designation=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        international_standard_book_number=dsl.Field(),
    ))

    @constituent_unit_entry.creator('marc', '774..')
    @utils.for_each_value
    @utils.filter_values
    def constituent_unit_entry(self, value):
        return {
            'relationship_code': value.get('4'),
            'control_subfield': value.get('7'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'main_entry_heading': value.get('a'),
            'qualifying_information': value.get('c'),
            'edition': value.get('b'),
            'place_publisher_and_date_of_publication': value.get('d'),
            'related_parts': value.get('g'),
            'relationship_information': value.get('i'),
            'physical_description': value.get('h'),
            'series_data_for_related_item': value.get('k'),
            'material_specific_details': value.get('m'),
            'other_item_identifier': value.get('o'),
            'note': value.get('n'),
            'uniform_title': value.get('s'),
            'report_number': value.get('r'),
            'standard_technical_report_number': value.get('u'),
            'title': value.get('t'),
            'record_control_number': value.get('w'),
            'coden_designation': value.get('y'),
            'international_standard_serial_number': value.get('x'),
            'international_standard_book_number': value.get('z')}

    other_edition_entry = dsl.List(dsl.Object(
        relationship_code=dsl.Field(),
        control_subfield=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        main_entry_heading=dsl.Field(),
        qualifying_information=dsl.Field(),
        edition=dsl.Field(),
        language_code=dsl.Field(),
        place_publisher_and_date_of_publication=dsl.Field(),
        related_parts=dsl.Field(),
        country_code=dsl.Field(),
        relationship_information=dsl.Field(),
        physical_description=dsl.Field(),
        series_data_for_related_item=dsl.Field(),
        material_specific_details=dsl.Field(),
        other_item_identifier=dsl.Field(),
        note=dsl.Field(),
        uniform_title=dsl.Field(),
        report_number=dsl.Field(),
        standard_technical_report_number=dsl.Field(),
        title=dsl.Field(),
        record_control_number=dsl.Field(),
        coden_designation=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        international_standard_book_number=dsl.Field(),
    ))

    @other_edition_entry.creator('marc', '775..')
    @utils.for_each_value
    @utils.filter_values
    def other_edition_entry(self, value):
        return {
            'relationship_code': value.get('4'),
            'control_subfield': value.get('7'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'main_entry_heading': value.get('a'),
            'qualifying_information': value.get('c'),
            'edition': value.get('b'),
            'language_code': value.get('e'),
            'place_publisher_and_date_of_publication': value.get('d'),
            'related_parts': value.get('g'),
            'country_code': value.get('f'),
            'relationship_information': value.get('i'),
            'physical_description': value.get('h'),
            'series_data_for_related_item': value.get('k'),
            'material_specific_details': value.get('m'),
            'other_item_identifier': value.get('o'),
            'note': value.get('n'),
            'uniform_title': value.get('s'),
            'report_number': value.get('r'),
            'standard_technical_report_number': value.get('u'),
            'title': value.get('t'),
            'record_control_number': value.get('w'),
            'coden_designation': value.get('y'),
            'international_standard_serial_number': value.get('x'),
            'international_standard_book_number': value.get('z')}

    additional_physical_form_entry = dsl.List(dsl.Object(
        relationship_code=dsl.Field(),
        control_subfield=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        main_entry_heading=dsl.Field(),
        qualifying_information=dsl.Field(),
        edition=dsl.Field(),
        place_publisher_and_date_of_publication=dsl.Field(),
        related_parts=dsl.Field(),
        relationship_information=dsl.Field(),
        physical_description=dsl.Field(),
        series_data_for_related_item=dsl.Field(),
        material_specific_details=dsl.Field(),
        other_item_identifier=dsl.Field(),
        note=dsl.Field(),
        uniform_title=dsl.Field(),
        report_number=dsl.Field(),
        standard_technical_report_number=dsl.Field(),
        title=dsl.Field(),
        record_control_number=dsl.Field(),
        coden_designation=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        international_standard_book_number=dsl.Field(),
    ))

    @additional_physical_form_entry.creator('marc', '776..')
    @utils.for_each_value
    @utils.filter_values
    def additional_physical_form_entry(self, value):
        return {
            'relationship_code': value.get('4'),
            'control_subfield': value.get('7'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'main_entry_heading': value.get('a'),
            'qualifying_information': value.get('c'),
            'edition': value.get('b'),
            'place_publisher_and_date_of_publication': value.get('d'),
            'related_parts': value.get('g'),
            'relationship_information': value.get('i'),
            'physical_description': value.get('h'),
            'series_data_for_related_item': value.get('k'),
            'material_specific_details': value.get('m'),
            'other_item_identifier': value.get('o'),
            'note': value.get('n'),
            'uniform_title': value.get('s'),
            'report_number': value.get('r'),
            'standard_technical_report_number': value.get('u'),
            'title': value.get('t'),
            'record_control_number': value.get('w'),
            'coden_designation': value.get('y'),
            'international_standard_serial_number': value.get('x'),
            'international_standard_book_number': value.get('z')}

    issued_with_entry = dsl.List(dsl.Object(
        main_entry_heading=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        qualifying_information=dsl.Field(),
        edition=dsl.Field(),
        place_publisher_and_date_of_publication=dsl.Field(),
        related_parts=dsl.Field(),
        relationship_information=dsl.Field(),
        physical_description=dsl.Field(),
        series_data_for_related_item=dsl.Field(),
        material_specific_details=dsl.Field(),
        other_item_identifier=dsl.Field(),
        note=dsl.Field(),
        record_control_number=dsl.Field(),
        uniform_title=dsl.Field(),
        relationship_code=dsl.Field(),
        control_subfield=dsl.Field(),
        linkage=dsl.Field(),
        coden_designation=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        title=dsl.Field(),
    ))

    @issued_with_entry.creator('marc', '777..')
    @utils.for_each_value
    @utils.filter_values
    def issued_with_entry(self, value):
        return {
            'main_entry_heading': value.get('a'),
            'international_standard_serial_number': value.get('x'),
            'qualifying_information': value.get('c'),
            'edition': value.get('b'),
            'place_publisher_and_date_of_publication': value.get('d'),
            'related_parts': value.get('g'),
            'relationship_information': value.get('i'),
            'physical_description': value.get('h'),
            'series_data_for_related_item': value.get('k'),
            'material_specific_details': value.get('m'),
            'other_item_identifier': value.get('o'),
            'note': value.get('n'),
            'record_control_number': value.get('w'),
            'uniform_title': value.get('s'),
            'relationship_code': value.get('4'),
            'control_subfield': value.get('7'),
            'linkage': value.get('6'),
            'coden_designation': value.get('y'),
            'field_link_and_sequence_number': value.get('8'),
            'title': value.get('t')}

    preceding_entry = dsl.List(dsl.Object(
        relationship_code=dsl.Field(),
        control_subfield=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        main_entry_heading=dsl.Field(),
        qualifying_information=dsl.Field(),
        edition=dsl.Field(),
        place_publisher_and_date_of_publication=dsl.Field(),
        related_parts=dsl.Field(),
        relationship_information=dsl.Field(),
        physical_description=dsl.Field(),
        series_data_for_related_item=dsl.Field(),
        material_specific_details=dsl.Field(),
        other_item_identifier=dsl.Field(),
        note=dsl.Field(),
        uniform_title=dsl.Field(),
        report_number=dsl.Field(),
        standard_technical_report_number=dsl.Field(),
        title=dsl.Field(),
        record_control_number=dsl.Field(),
        coden_designation=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        international_standard_book_number=dsl.Field(),
    ))

    @preceding_entry.creator('marc', '780..')
    @utils.for_each_value
    @utils.filter_values
    def preceding_entry(self, value):
        return {
            'relationship_code': value.get('4'),
            'control_subfield': value.get('7'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'main_entry_heading': value.get('a'),
            'qualifying_information': value.get('c'),
            'edition': value.get('b'),
            'place_publisher_and_date_of_publication': value.get('d'),
            'related_parts': value.get('g'),
            'relationship_information': value.get('i'),
            'physical_description': value.get('h'),
            'series_data_for_related_item': value.get('k'),
            'material_specific_details': value.get('m'),
            'other_item_identifier': value.get('o'),
            'note': value.get('n'),
            'uniform_title': value.get('s'),
            'report_number': value.get('r'),
            'standard_technical_report_number': value.get('u'),
            'title': value.get('t'),
            'record_control_number': value.get('w'),
            'coden_designation': value.get('y'),
            'international_standard_serial_number': value.get('x'),
            'international_standard_book_number': value.get('z')}

    succeeding_entry = dsl.List(dsl.Object(
        relationship_code=dsl.Field(),
        control_subfield=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        main_entry_heading=dsl.Field(),
        qualifying_information=dsl.Field(),
        edition=dsl.Field(),
        place_publisher_and_date_of_publication=dsl.Field(),
        related_parts=dsl.Field(),
        relationship_information=dsl.Field(),
        physical_description=dsl.Field(),
        series_data_for_related_item=dsl.Field(),
        material_specific_details=dsl.Field(),
        other_item_identifier=dsl.Field(),
        note=dsl.Field(),
        uniform_title=dsl.Field(),
        report_number=dsl.Field(),
        standard_technical_report_number=dsl.Field(),
        title=dsl.Field(),
        record_control_number=dsl.Field(),
        coden_designation=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        international_standard_book_number=dsl.Field(),
    ))

    @succeeding_entry.creator('marc', '785..')
    @utils.for_each_value
    @utils.filter_values
    def succeeding_entry(self, value):
        return {
            'relationship_code': value.get('4'),
            'control_subfield': value.get('7'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'main_entry_heading': value.get('a'),
            'qualifying_information': value.get('c'),
            'edition': value.get('b'),
            'place_publisher_and_date_of_publication': value.get('d'),
            'related_parts': value.get('g'),
            'relationship_information': value.get('i'),
            'physical_description': value.get('h'),
            'series_data_for_related_item': value.get('k'),
            'material_specific_details': value.get('m'),
            'other_item_identifier': value.get('o'),
            'note': value.get('n'),
            'uniform_title': value.get('s'),
            'report_number': value.get('r'),
            'standard_technical_report_number': value.get('u'),
            'title': value.get('t'),
            'record_control_number': value.get('w'),
            'coden_designation': value.get('y'),
            'international_standard_serial_number': value.get('x'),
            'international_standard_book_number': value.get('z')}

    data_source_entry = dsl.List(dsl.Object(
        relationship_code=dsl.Field(),
        control_subfield=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        main_entry_heading=dsl.Field(),
        qualifying_information=dsl.Field(),
        edition=dsl.Field(),
        place_publisher_and_date_of_publication=dsl.Field(),
        related_parts=dsl.Field(),
        relationship_information=dsl.Field(),
        physical_description=dsl.Field(),
        series_data_for_related_item=dsl.Field(),
        period_of_content=dsl.Field(),
        material_specific_details=dsl.Field(),
        other_item_identifier=dsl.Field(),
        note=dsl.Field(),
        abbreviated_title=dsl.Field(),
        uniform_title=dsl.Field(),
        report_number=dsl.Field(),
        standard_technical_report_number=dsl.Field(),
        title=dsl.Field(),
        record_control_number=dsl.Field(),
        source_contribution=dsl.Field(),
        coden_designation=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        international_standard_book_number=dsl.Field(),
    ))

    @data_source_entry.creator('marc', '786..')
    @utils.for_each_value
    @utils.filter_values
    def data_source_entry(self, value):
        return {
            'relationship_code': value.get('4'),
            'control_subfield': value.get('7'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'main_entry_heading': value.get('a'),
            'qualifying_information': value.get('c'),
            'edition': value.get('b'),
            'place_publisher_and_date_of_publication': value.get('d'),
            'related_parts': value.get('g'),
            'relationship_information': value.get('i'),
            'physical_description': value.get('h'),
            'series_data_for_related_item': value.get('k'),
            'period_of_content': value.get('j'),
            'material_specific_details': value.get('m'),
            'other_item_identifier': value.get('o'),
            'note': value.get('n'),
            'abbreviated_title': value.get('p'),
            'uniform_title': value.get('s'),
            'report_number': value.get('r'),
            'standard_technical_report_number': value.get('u'),
            'title': value.get('t'),
            'record_control_number': value.get('w'),
            'source_contribution': value.get('v'),
            'coden_designation': value.get('y'),
            'international_standard_serial_number': value.get('x'),
            'international_standard_book_number': value.get('z')}

    other_relationship_entry = dsl.List(dsl.Object(
        relationship_code=dsl.Field(),
        control_subfield=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        main_entry_heading=dsl.Field(),
        qualifying_information=dsl.Field(),
        edition=dsl.Field(),
        place_publisher_and_date_of_publication=dsl.Field(),
        related_parts=dsl.Field(),
        relationship_information=dsl.Field(),
        physical_description=dsl.Field(),
        series_data_for_related_item=dsl.Field(),
        material_specific_details=dsl.Field(),
        other_item_identifier=dsl.Field(),
        note=dsl.Field(),
        uniform_title=dsl.Field(),
        report_number=dsl.Field(),
        standard_technical_report_number=dsl.Field(),
        title=dsl.Field(),
        record_control_number=dsl.Field(),
        coden_designation=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
        international_standard_book_number=dsl.Field(),
    ))

    @other_relationship_entry.creator('marc', '787..')
    @utils.for_each_value
    @utils.filter_values
    def other_relationship_entry(self, value):
        return {
            'relationship_code': value.get('4'),
            'control_subfield': value.get('7'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'main_entry_heading': value.get('a'),
            'qualifying_information': value.get('c'),
            'edition': value.get('b'),
            'place_publisher_and_date_of_publication': value.get('d'),
            'related_parts': value.get('g'),
            'relationship_information': value.get('i'),
            'physical_description': value.get('h'),
            'series_data_for_related_item': value.get('k'),
            'material_specific_details': value.get('m'),
            'other_item_identifier': value.get('o'),
            'note': value.get('n'),
            'uniform_title': value.get('s'),
            'report_number': value.get('r'),
            'standard_technical_report_number': value.get('u'),
            'title': value.get('t'),
            'record_control_number': value.get('w'),
            'coden_designation': value.get('y'),
            'international_standard_serial_number': value.get('x'),
            'international_standard_book_number': value.get('z')}

    series_added_entry_personal_name = dsl.List(dsl.Object(
        authority_record_control_number=dsl.Field(),
        materials_specified=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        relator_code=dsl.Field(),
        control_subfield=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        personal_name=dsl.Field(),
        titles_and_other_words_associated_with_a_name=dsl.Field(),
        numeration=dsl.Field(),
        relator_term=dsl.Field(),
        dates_associated_with_a_name=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_of_a_work=dsl.Field(),
        medium=dsl.Field(),
        form_subheading=dsl.Field(),
        attribution_qualifier=dsl.Field(),
        medium_of_performance_for_music=dsl.Field(),
        language_of_a_work=dsl.Field(),
        arranged_statement_for_music=dsl.Field(),
        number_of_part_section_of_a_work=dsl.Field(),
        fuller_form_of_name=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        version=dsl.Field(),
        key_for_music=dsl.Field(),
        affiliation=dsl.Field(),
        title_of_a_work=dsl.Field(),
        bibliographic_record_control_number=dsl.Field(),
        volume_sequential_designation=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
    ))

    @series_added_entry_personal_name.creator('marc', '800..')
    @utils.for_each_value
    @utils.filter_values
    def series_added_entry_personal_name(self, value):
        return {
            'authority_record_control_number': value.get('0'),
            'materials_specified': value.get('3'),
            'institution_to_which_field_applies': value.get('5'),
            'relator_code': value.get('4'),
            'control_subfield': value.get('7'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'personal_name': value.get('a'),
            'titles_and_other_words_associated_with_a_name': value.get('c'),
            'numeration': value.get('b'),
            'relator_term': value.get('e'),
            'dates_associated_with_a_name': value.get('d'),
            'miscellaneous_information': value.get('g'),
            'date_of_a_work': value.get('f'),
            'medium': value.get('h'),
            'form_subheading': value.get('k'),
            'attribution_qualifier': value.get('j'),
            'medium_of_performance_for_music': value.get('m'),
            'language_of_a_work': value.get('l'),
            'arranged_statement_for_music': value.get('o'),
            'number_of_part_section_of_a_work': value.get('n'),
            'fuller_form_of_name': value.get('q'),
            'name_of_part_section_of_a_work': value.get('p'),
            'version': value.get('s'),
            'key_for_music': value.get('r'),
            'affiliation': value.get('u'),
            'title_of_a_work': value.get('t'),
            'bibliographic_record_control_number': value.get('w'),
            'volume_sequential_designation': value.get('v'),
            'international_standard_serial_number': value.get('x')}

    series_added_entry_corporate_name = dsl.List(dsl.Object(
        authority_record_control_number=dsl.Field(),
        materials_specified=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        relator_code=dsl.Field(),
        control_subfield=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        corporate_name_or_jurisdiction_name_as_entry_element=dsl.Field(),
        location_of_meeting=dsl.Field(),
        subordinate_unit=dsl.Field(),
        relator_term=dsl.Field(),
        date_of_meeting_or_treaty_signing=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_of_a_work=dsl.Field(),
        medium=dsl.Field(),
        form_subheading=dsl.Field(),
        medium_of_performance_for_music=dsl.Field(),
        language_of_a_work=dsl.Field(),
        arranged_statement_for_music=dsl.Field(),
        number_of_part_section_meeting=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        version=dsl.Field(),
        key_for_music=dsl.Field(),
        affiliation=dsl.Field(),
        title_of_a_work=dsl.Field(),
        bibliographic_record_control_number=dsl.Field(),
        volume_sequential_designation=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
    ))

    @series_added_entry_corporate_name.creator('marc', '810..')
    @utils.for_each_value
    @utils.filter_values
    def series_added_entry_corporate_name(self, value):
        return {
            'authority_record_control_number': value.get('0'),
            'materials_specified': value.get('3'),
            'institution_to_which_field_applies': value.get('5'),
            'relator_code': value.get('4'),
            'control_subfield': value.get('7'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'corporate_name_or_jurisdiction_name_as_entry_element': value.get('a'),
            'location_of_meeting': value.get('c'),
            'subordinate_unit': value.get('b'),
            'relator_term': value.get('e'),
            'date_of_meeting_or_treaty_signing': value.get('d'),
            'miscellaneous_information': value.get('g'),
            'date_of_a_work': value.get('f'),
            'medium': value.get('h'),
            'form_subheading': value.get('k'),
            'medium_of_performance_for_music': value.get('m'),
            'language_of_a_work': value.get('l'),
            'arranged_statement_for_music': value.get('o'),
            'number_of_part_section_meeting': value.get('n'),
            'name_of_part_section_of_a_work': value.get('p'),
            'version': value.get('s'),
            'key_for_music': value.get('r'),
            'affiliation': value.get('u'),
            'title_of_a_work': value.get('t'),
            'bibliographic_record_control_number': value.get('w'),
            'volume_sequential_designation': value.get('v'),
            'international_standard_serial_number': value.get('x')}

    series_added_entry_meeting_name = dsl.List(dsl.Object(
        authority_record_control_number=dsl.Field(),
        materials_specified=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        relator_code=dsl.Field(),
        control_subfield=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        meeting_name_or_jurisdiction_name_as_entry_element=dsl.Field(),
        location_of_meeting=dsl.Field(),
        subordinate_unit=dsl.Field(),
        date_of_meeting=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_of_a_work=dsl.Field(),
        medium=dsl.Field(),
        form_subheading=dsl.Field(),
        relator_term=dsl.Field(),
        language_of_a_work=dsl.Field(),
        number_of_part_section_meeting=dsl.Field(),
        name_of_meeting_following_jurisdiction_name_entry_element=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        version=dsl.Field(),
        affiliation=dsl.Field(),
        title_of_a_work=dsl.Field(),
        bibliographic_record_control_number=dsl.Field(),
        volume_sequential_designation=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
    ))

    @series_added_entry_meeting_name.creator('marc', '811..')
    @utils.for_each_value
    @utils.filter_values
    def series_added_entry_meeting_name(self, value):
        return {
            'authority_record_control_number': value.get('0'),
            'materials_specified': value.get('3'),
            'institution_to_which_field_applies': value.get('5'),
            'relator_code': value.get('4'),
            'control_subfield': value.get('7'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'meeting_name_or_jurisdiction_name_as_entry_element': value.get('a'),
            'location_of_meeting': value.get('c'),
            'subordinate_unit': value.get('e'),
            'date_of_meeting': value.get('d'),
            'miscellaneous_information': value.get('g'),
            'date_of_a_work': value.get('f'),
            'medium': value.get('h'),
            'form_subheading': value.get('k'),
            'relator_term': value.get('j'),
            'language_of_a_work': value.get('l'),
            'number_of_part_section_meeting': value.get('n'),
            'name_of_meeting_following_jurisdiction_name_entry_element': value.get('q'),
            'name_of_part_section_of_a_work': value.get('p'),
            'version': value.get('s'),
            'affiliation': value.get('u'),
            'title_of_a_work': value.get('t'),
            'bibliographic_record_control_number': value.get('w'),
            'volume_sequential_designation': value.get('v'),
            'international_standard_serial_number': value.get('x')}

    series_added_entry_uniform_title = dsl.List(dsl.Object(
        authority_record_control_number=dsl.Field(),
        materials_specified=dsl.Field(),
        institution_to_which_field_applies=dsl.Field(),
        control_subfield=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        uniform_title=dsl.Field(),
        date_of_treaty_signing=dsl.Field(),
        miscellaneous_information=dsl.Field(),
        date_of_a_work=dsl.Field(),
        medium=dsl.Field(),
        form_subheading=dsl.Field(),
        medium_of_performance_for_music=dsl.Field(),
        language_of_a_work=dsl.Field(),
        arranged_statement_for_music=dsl.Field(),
        number_of_part_section_of_a_work=dsl.Field(),
        name_of_part_section_of_a_work=dsl.Field(),
        version=dsl.Field(),
        key_for_music=dsl.Field(),
        title_of_a_work=dsl.Field(),
        bibliographic_record_control_number=dsl.Field(),
        volume_sequential_designation=dsl.Field(),
        international_standard_serial_number=dsl.Field(),
    ))

    @series_added_entry_uniform_title.creator('marc', '830..')
    @utils.for_each_value
    @utils.filter_values
    def series_added_entry_uniform_title(self, value):
        return {
            'authority_record_control_number': value.get('0'),
            'materials_specified': value.get('3'),
            'institution_to_which_field_applies': value.get('5'),
            'control_subfield': value.get('7'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'uniform_title': value.get('a'),
            'date_of_treaty_signing': value.get('d'),
            'miscellaneous_information': value.get('g'),
            'date_of_a_work': value.get('f'),
            'medium': value.get('h'),
            'form_subheading': value.get('k'),
            'medium_of_performance_for_music': value.get('m'),
            'language_of_a_work': value.get('l'),
            'arranged_statement_for_music': value.get('o'),
            'number_of_part_section_of_a_work': value.get('n'),
            'name_of_part_section_of_a_work': value.get('p'),
            'version': value.get('s'),
            'key_for_music': value.get('r'),
            'title_of_a_work': value.get('t'),
            'bibliographic_record_control_number': value.get('w'),
            'volume_sequential_designation': value.get('v'),
            'international_standard_serial_number': value.get('x')}

    holding_institution = dsl.List(dsl.Object(
        holding_institution=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @holding_institution.creator('marc', '850..')
    @utils.for_each_value
    @utils.filter_values
    def holding_institution(self, value):
        return {
            'holding_institution': value.get('a'),
            'field_link_and_sequence_number': value.get('8')}

    location = dsl.List(dsl.Object(
        materials_specified=dsl.Field(),
        source_of_classification_or_shelving_scheme=dsl.Field(),
        linkage=dsl.Field(),
        sequence_number=dsl.Field(),
        location=dsl.Field(),
        shelving_location=dsl.Field(),
        sublocation_or_collection=dsl.Field(),
        address=dsl.Field(),
        former_shelving_location=dsl.Field(),
        non_coded_location_qualifier=dsl.Field(),
        coded_location_qualifier=dsl.Field(),
        item_part=dsl.Field(),
        classification_part=dsl.Field(),
        call_number_prefix=dsl.Field(),
        shelving_control_number=dsl.Field(),
        call_number_suffix=dsl.Field(),
        shelving_form_of_title=dsl.Field(),
        country_code=dsl.Field(),
        piece_physical_condition=dsl.Field(),
        piece_designation=dsl.Field(),
        copyright_article_fee_code=dsl.Field(),
        uniform_resource_identifier=dsl.Field(),
        copy_number=dsl.Field(),
        nonpublic_note=dsl.Field(),
        public_note=dsl.Field(),
    ))

    @location.creator('marc', '852..')
    @utils.for_each_value
    @utils.filter_values
    def location(self, value):
        return {
            'materials_specified': value.get('3'),
            'source_of_classification_or_shelving_scheme': value.get('2'),
            'linkage': value.get('6'),
            'sequence_number': value.get('8'),
            'location': value.get('a'),
            'shelving_location': value.get('c'),
            'sublocation_or_collection': value.get('b'),
            'address': value.get('e'),
            'former_shelving_location': value.get('d'),
            'non_coded_location_qualifier': value.get('g'),
            'coded_location_qualifier': value.get('f'),
            'item_part': value.get('i'),
            'classification_part': value.get('h'),
            'call_number_prefix': value.get('k'),
            'shelving_control_number': value.get('j'),
            'call_number_suffix': value.get('m'),
            'shelving_form_of_title': value.get('l'),
            'country_code': value.get('n'),
            'piece_physical_condition': value.get('q'),
            'piece_designation': value.get('p'),
            'copyright_article_fee_code': value.get('s'),
            'uniform_resource_identifier': value.get('u'),
            'copy_number': value.get('t'),
            'nonpublic_note': value.get('x'),
            'public_note': value.get('z')}

    electronic_location_and_access = dsl.List(dsl.Object(
        materials_specified=dsl.Field(),
        access_method=dsl.Field(),
        linkage=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        host_name=dsl.Field(),
        compression_information=dsl.Field(),
        access_number=dsl.Field(),
        path=dsl.Field(),
        electronic_name=dsl.Field(),
        instruction=dsl.Field(),
        processor_of_request=dsl.Field(),
        password=dsl.Field(),
        bits_per_second=dsl.Field(),
        contact_for_access_assistance=dsl.Field(),
        logon=dsl.Field(),
        operating_system=dsl.Field(),
        name_of_location_of_host=dsl.Field(),
        electronic_format_type=dsl.Field(),
        port=dsl.Field(),
        file_size=dsl.Field(),
        settings=dsl.Field(),
        uniform_resource_identifier=dsl.Field(),
        terminal_emulation=dsl.Field(),
        record_control_number=dsl.Field(),
        hours_access_method_available=dsl.Field(),
        link_text=dsl.Field(),
        nonpublic_note=dsl.Field(),
        public_note=dsl.Field(),
    ))

    @electronic_location_and_access.creator('marc', '856..')
    @utils.for_each_value
    @utils.filter_values
    def electronic_location_and_access(self, value):
        return {
            'materials_specified': value.get('3'),
            'access_method': value.get('2'),
            'linkage': value.get('6'),
            'field_link_and_sequence_number': value.get('8'),
            'host_name': value.get('a'),
            'compression_information': value.get('c'),
            'access_number': value.get('b'),
            'path': value.get('d'),
            'electronic_name': value.get('f'),
            'instruction': value.get('i'),
            'processor_of_request': value.get('h'),
            'password': value.get('k'),
            'bits_per_second': value.get('j'),
            'contact_for_access_assistance': value.get('m'),
            'logon': value.get('l'),
            'operating_system': value.get('o'),
            'name_of_location_of_host': value.get('n'),
            'electronic_format_type': value.get('q'),
            'port': value.get('p'),
            'file_size': value.get('s'),
            'settings': value.get('r'),
            'uniform_resource_identifier': value.get('u'),
            'terminal_emulation': value.get('t'),
            'record_control_number': value.get('w'),
            'hours_access_method_available': value.get('v'),
            'link_text': value.get('y'),
            'nonpublic_note': value.get('x'),
            'public_note': value.get('z')}

    replacement_record_information = dsl.Object(
        replacement_title=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
        explanatory_text=dsl.Field(),
        replacement_bibliographic_record_control_number=dsl.Field(),
        linkage=dsl.Field(),
    )

    @replacement_record_information.creator('marc', '882..')
    @utils.filter_values
    def replacement_record_information(self, value):
        return {
            'replacement_title': value.get('a'),
            'field_link_and_sequence_number': value.get('8'),
            'explanatory_text': value.get('i'),
            'replacement_bibliographic_record_control_number': value.get('w'),
            'linkage': value.get('6')}

    machine_generated_metadata_provenance = dsl.List(dsl.Object(
        generation_process=dsl.Field(),
        confidence_value=dsl.Field(),
        generation_date=dsl.Field(),
        generation_agency=dsl.Field(),
        authority_record_control_number_or_standard_number=dsl.Field(),
        uniform_resource_identifier=dsl.Field(),
        bibliographic_record_control_number=dsl.Field(),
        validity_end_date=dsl.Field(),
        field_link_and_sequence_number=dsl.Field(),
    ))

    @machine_generated_metadata_provenance.creator('marc', '883..')
    @utils.for_each_value
    @utils.filter_values
    def machine_generated_metadata_provenance(self, value):
        return {
            'generation_process': value.get('a'),
            'confidence_value': value.get('c'),
            'generation_date': value.get('d'),
            'generation_agency': value.get('q'),
            'authority_record_control_number_or_standard_number': value.get('0'),
            'uniform_resource_identifier': value.get('u'),
            'bibliographic_record_control_number': value.get('w'),
            'validity_end_date': value.get('x'),
            'field_link_and_sequence_number': value.get('8')}

    non_marc_information_field = dsl.List(dsl.Object(
        content_of_non_marc_field=dsl.Field(),
        source_of_data=dsl.Field(),
    ))

    @non_marc_information_field.creator('marc', '887..')
    @utils.for_each_value
    @utils.filter_values
    def non_marc_information_field(self, value):
        return {
            'content_of_non_marc_field': value.get('a'),
            'source_of_data': value.get('2')}
