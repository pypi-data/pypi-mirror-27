from base import FEIWSBaseClient

#TODO Depricate client 10
#TODO implement Commen WebService Method in client
#TODO refactor client11 to just client


class FEIWSClient(FEIWSBaseClient):
    def __init__(self, username=None, password=None):
        super(FEIWSClient, self).__init__((1, 2), username, password)

    def find_athlete(self, fei_ids=None, family_name=None, first_name=None,
                     gender_code=None, competing_for=None):
        """Find athletes based on a certain search criteria.

        Params:
            fei_ids: A tuple of Athlete FEI IDs you want to search for.
            family_name: The athlete's family name. Use % to create a `contain`
             query
            first_name: The athlete's first name. User % to create a `contain`
             query
            gender_code: The athlete gender(None=All, M=Male, F=Female)
            competing_for: The NOC code of the athlete's country he is competing
             for

        Return value: An array of Athlete objects.

        """
        fei_ids_array = None
        if fei_ids:
            fei_ids_array = self._ows_factory.ArrayOfString(string=fei_ids)
        result = self._ows_client.service.findAthlete(FEIIDs=fei_ids_array, FamilyName=family_name, FirstName=first_name,
                                                      GenderCode=gender_code, CompetingFor=competing_for)
        self._handle_messages(result)
        return result.body.findAthleteResult.AthleteOC if hasattr(result.body.findAthleteResult, 'AthleteOC') else []

    def find_official(self, any_id=None, any_name=None, person_gender=None,
                     admin_nf=None, person_status=None, official_function=None,
                     official_function_discipline=None):
        """Find officials based on a certain search criteria.

        Params:
            any_id: Return officials having this ID, licence nr, or vet delegat nr.
            any_name: Return officials having this family name, first name, nick name.
                use % to make a `contain` search.
            person_gender: Return officials with this gender
            admin_nf: Return official that are member of the administrative NF
            person_status: Return the official having this status:
                10: Search for all competitors
                1: Search only for active competitors
                0: Search only for inactive competitors
                2: Search only for pending competitors
                3: Search only for cancelled competitors
                9: Search only for suspended competitors.
            official_function: Search for officials with specified function
            official_function_discipline: Return officials having the specified official
                function for this discipline.

        Return value: An array of PersonOfficialOC objects
        """
        result = self._ows_client.service.findOfficial(
            AnyID=any_id, AnyName=any_name, PersonGender=person_gender, AdminNF=admin_nf,
            PersonStatus=person_status, OfficialFunction=official_function,
            OfficialFunctionDiscipline=official_function_discipline)
        self._handle_messages(result)
        if hasattr(result.body.findOfficialResult, 'PersonOfficialOC'):
            return result.body.findOfficialResult.PersonOfficialOC
        return []

    def find_horse(self, fei_ids=None, name=None, sex_code=None, is_pony=None,
                   athlete_fei_id=None):
        """Find horses based on a certain search criteria.

        Params:
            fei_ids: A tuple of Horse FEI IDs you want to search for.
            name: The name of the horse. Use % to create a contain query
            sex_code: The sex code of the horse (None=All, F=Mare, G=Gelding,
                S=Stallion, M=Male Unknown, U=Unknown).
            is_pony: Boolean indicating to search for only ponies.
            athlete_fei_id: Search for horses associated with this Athlete.

        Return value: A list of Horse objects.

        """
        fei_ids_array = None
        if fei_ids:
            fei_ids_array = self._ows_factory.ArrayOfString(string=fei_ids)
        result = self._ows_client.service.findHorse(
            FEIIDs=fei_ids_array, Name=name, SexCode=sex_code, IsPony=is_pony,
            AthleteFEIID=athlete_fei_id)
        self._handle_messages(result)
        return result.body.findHorseResult.HorseOC if hasattr(result.body.findHorseResult, 'HorseOC') else []

    def search_horse_trainers(self, horse_fei_code=None, person_fei_id=None, eval_date=None, page_number=1):
        """
        Search for horse trainer records

        :param horse_fei_code: The FEI identifier of the horse filters the records and returns only trainers
        linked to this horse. It maybe null.
        :param person_fei_id: The FEI identifier of the person filters the records and returns only the trainer
        having this ID. It may be null
        :param eval_date: The evaluation date filters the horse trainer records and returns only those whose period
        is active at this evaluation date. It may be null.
        :param page_number: Which page to retrieve. 1 = 1 - 100, 2 = 101 - 200
        :return: returns an array of zero or more HorseTrainer objects.
        """

        result = self._ows_client.service.searchHorseTrainers(
            HorseFEICode=horse_fei_code, PersonFEIID=person_fei_id, EvalDate=eval_date, PageNumber=page_number)
        self._handle_messages(result)
        if hasattr(result.body.searchHorseTrainersResult, 'HorseTrainer'):
            return result.body.searchHorseTrainersResult.HorseTrainer
        return[]

    def find_event(self, id='', show_date_from=None, show_date_to=None, venue_name='', nf='', discipline_code='',
                   level_code='', is_indoor=None):
        """Find FEI events based on a certain search criteria.

        Params:
            id: FEI show/event/competition ID.
            show_date_from: Filter shows from this date up.
            show_date_to: Filter shows from this date down.
            venue_name: The name of the place where the show is held.
            nf: Country code of the national federation.
            discipline_code: Filter shows based on discipline.
            level_code: Filter shows based on level.
            is_indoor: Filter indoor / outdoor shows.

        Return value: A list of FEI events

        """
        result = self._ows_client.service.findEvent(
            id, show_date_from, show_date_to, venue_name, nf, discipline_code,
            level_code, is_indoor)
        self._handle_messages(result)
        return result.body.findEventResult.ShowOC

    def download_results(self, id):
        """Download XML results from the FEI. (You need permission from the FEI
         to download results from an event.

        Params:
            id: FEI event/competition ID.

        Return value: A string containing the information in FEI XML.

        """
        result = self._ows_client.service.downloadResults(id)
        self._handle_messages(result)
        return result

    def upload_results(self, result_xml_data):
        """Upload results to the FEI. (You need permission from the FEI to
        upload results to the FEI.

        Params:
            result_xml_data = Base64Encoded FEI result file.

        Return value:
            FileID = can be used to confirm uploaded results
            Results = String indicating if the uploaded succeeded.
                ERR = An error was found while processing the validation
                MAN = An error was found while processing the mandotory check
                OKW = It is ok for saving, but there are warnings
                OKD = the saving has been done

        """
        return self._ows_client.service.uploadResults(result_xml_data)

    def confirm_upload_results(self, file_id):
        """Confirm uploaded results. This is only needed when results returned
         OK with warnings.

        Params:
            file_id: The FileID return by the uploadResults routine.

        Return value: True if the saving has been done.

        """
        return self._ows_client.service.confirmUploadResults(file_id)

    def submit_results(self, id):
        """Submit the results to the FEI validation for a given event or a
         given competition.

        Params:
            id: FEI event/competition ID.

        Return value: True if the results have been successfully submitted.

        """
        return self._ows_client.service.submitResults(id)

    def get_version(self):
        """
        Return the version string of the Core Application software
        :return: Returns a string containing the [major.minor.revision] number.
        If no return value is recieved or the call times out then the web service is not working
        and should not be used.
        """
        return self._cs_client.service.getVersion().body.getVersionResult

    def get_lookup_date_list(self):
        """
        Retrieve a list of cached information types, and the date each was last modified.
        :return: Returns an array of LookupDate objects.
        Each LookupDate object contains the name of an object type and the most recent date of modification
        for any of the lookup records held in that object type. Client applications should keep these
        lookup records in a local cache to improve performance, and reduce server load.
        For each of these LookupDate objects, there is a corresponding method get<LookupDate.Name>List()
        that retrieves a list of all records of that type.
        """
        result = self._cs_client.service.getLookupDateList()
        if hasattr(result.body.getLookupDateListResult, 'LookupDate'):
            return result.body.getLookupDateListResult
        return []
