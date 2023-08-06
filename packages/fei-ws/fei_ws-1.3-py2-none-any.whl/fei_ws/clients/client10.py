from base import FEIWSBaseClient


class FEIWSClient10(FEIWSBaseClient):
    def __init__(self, username=None, password=None):
        super(FEIWSClient10, self).__init__((1, 0), username, password)

    def getVersion(self):
        """Retrieve the current version

        Return value: A version number

        """
        return self._cs_client.service.getVersion()


    def getVenueList(self):
        """Retrieve a list of venues.

        Return value: An array of Venue objects

        """
        return self._ows_client.service.getVenueList()

    def getShowTypeList(self):
        """Retrieve a list of show types.

        Return value: An array of ShowType objects

        """
        return self._ows_client.service.getShowTypeList()

    def getShowRegionList(self):
        """Retrieve a list of region for the show.

        Return value: An array of ShowRegion objects
        """
        return self._ows_client.service.getShowRegionList()

    def searchForShow(self, NF=None, DateStart=None, DateEnd=None, Venue=None,
                      Discipline=None, EventCode=None, Indoor=None):
        """Search for shows matching a search criteria

        Params:
            NF: Search event from this National Federation.
            DateStart: Search from this datetime up.
            DateEnd: Search from this datetime down.
            Venue: Venue to search for.
            ShowType: Show type to search for.
            Discipline: Discipline to search for.
            EventCode: EventCode to search for.
            Indoor: Search for indoor events or outdoor(Boolean).

        Return Value: An array of zero or more Show objects.

        """
        sc = []
        factory = self._ows_client.factory
        if NF:
            criteria = factory.create('SCNFCode')
            criteria.NFCode = NF
            sc.append(criteria)
        if DateStart or DateEnd:
            criteria = factory.create('SCShowDates')
            criteria.DateStart = DateStart
            criteria.DateEnd = DateEnd
            sc.append(criteria)
        if Venue:
            criteria = factory.create('SCShowVenue')
            criteria.Value = Venue
            sc.append(criteria)
        if Discipline:
            criteria = factory.create('SCShowDiscipline')
            criteria.Value = Discipline
            sc.append(criteria)
        if EventCode:
            criteria = factory.create('SCShowEventCode')
            criteria.Value = EventCode
            sc.append(criteria)
        if Indoor:
            criteria = factory.create('SCShowIndoor')
            criteria.Value = Indoor
            sc.append(criteria)
        if not sc:
            raise Exception('MissingConditions: You need to supply at least '
                            'one search criteria')
        sc_array = factory.create('ArrayOfSCBase')
        sc_array.SCBase = sc
        result = self._ows_client.service.searchForShow(sc_array)
        self._handle_messages(result)
        return result.searchForShowResult

    def getEventsByShowCode(self, ShowCode):
        """Retrieve all records of event by using the code of the show.

        Params:
            ShowCode: Get events belonging to the show with this code

        Result value: Returns an array of Event objects, or None pointer if
         there is an error found.
        """
        result = self._ows_client.service.getEventsByShowCode(ShowCode)
        self._handle_messages(result)
        return result.getEventsByShowCodeResult

    def getShow(self, ShowCode):
        """Get a show by its code.

        Params:
            ShowCode: The code of the show you want to retrieve.

        Result value: A Show object or None if an error occurred or no
         show matched the code.

        """
        result = self._ows_client.service.getShow(ShowCode)
        self._handle_messages(result)
        return result.getShowResult

    def getShows(self, ShowCodes):
        """Get a list of shows by their ShowCode

        Params:
            ShowCodes: An array of show codes.

        Result value: An array of Show objects, or None when no match.

        """
        string_array = self._ows_client.factory.create('ArrayOfString')
        string_array.string = ShowCodes
        result = self._ows_client.service.getShows(string_array)
        self._handle_messages(result)
        return result.getShowsResult

    def getEventTypeCodeList(self):
        """Retrieve a list of available event type codes.

        Return value: An array of EventTypeCode objects

        """
        return self._ows_client.service.getEventTypeCodeList()

    def getEvent(self, EventCode):
        """Retrieve an Event by its EventCode

        Params:
            EventCode: The event code of the desired event

        Return value: An Event object or None

        """
        result = self._ows_client.service.getEvent(EventCode)
        self._handle_messages(result)
        return result.getEventResult

    def getEvents(self, EventCodes):
        """Get a list of events by their event codes

        Params:
            EventCodes: An array of event codes

        Return value: An array of Event objects or None

        """
        string_array = self._ows_client.factory.create('ArrayOfString')
        string_array.string = EventCodes
        result = self._ows_client.service.getEvents(string_array)
        self._handle_messages(result)
        return result.getEventsResult

    def searchForEvent(self, NF=None, DateStart=None, DateEnd=None, Venue=None,
                       Discipline=None, EventCode=None, Indoor=None):
        """Search for events matching a search criteria

        Params:
            NF: Search event from this National Federation.
            DateStart: Search from this datetime up.
            DateEnd: Search from this datetime down.
            Venue: Venue to search for.
            ShowType: Show type to search for.
            Discipline: Discipline to search for.
            EventCode: EventCode to search for.
            Indoor: Search for indoor events or outdoor(Boolean).

        Return Value: an array of Events or None

        """
        sc = []
        factory = self._ows_client.factory
        if NF:
            criteria = factory.create('SCNFCode')
            criteria.NFCode = NF
            sc.append(criteria)
        if DateStart or DateEnd:
            criteria = factory.create('SCShowDates')
            criteria.DateStart = DateStart
            criteria.DateEnd = DateEnd
            sc.append(criteria)
        if Venue:
            criteria = factory.create('SCShowVenue')
            criteria.Value = Venue
            sc.append(criteria)
        if Discipline:
            criteria = factory.create('SCShowDiscipline')
            criteria.Value = Discipline
            sc.append(criteria)
        if EventCode:
            criteria = factory.create('SCShowEventCode')
            criteria.Value = EventCode
            sc.append(criteria)
        if Indoor:
            criteria = factory.create('SCShowIndoor')
            criteria.Value = Indoor
            sc.append(criteria)
        if not sc:
            raise Exception('MissingConditions: You need to supply at least '
                            'one search criteria')
        sc_array = factory.create('ArrayOfSCBase')
        sc_array.SCBase = sc
        result = self._ows_client.service.searchForEvent(sc_array)
        self._handle_messages(result)
        return result.searchForEventResult

    def getEventResults(self, EventCode):
        """Retrieve a list of detailed results related to an event given
         by its code.

        Params:
            EventCode: The code of the event you want the results from.

        Return value: An array of NFResult

        """
        result = self._ows_client.service.getEventResults(EventCode)
        self._handle_messages(result)
        return result.getEventResultsResult

    def uploadEventResult(self, ResultsXMLData):
        """Save the result XML file for the given event

        Params:
            ResultsXMLData: The result xml file, byte formatted.
            OUT-> FIleID: Containing an integer corresponding with the file ID.

        Return value: a string containing one of the following statuses
            ERR: An error was found while processing the validation.
            MAN: An error was found while processing the mandatory check.
            OKW: Result accepted, but their are warnings.
            OKD: The saving has been done.

        """
        result = self._ows_client.service.uploadEventResult(ResultsXMLData)
        self._handle_messages(result)
        return result

    def saveEventResults(self, FileID):
        """Save the event results after user confirmation.

        Params:
            FileID: The FileID corresponding with the upload you want to save

        Return value: True if the saving is done
        """
        result = self._ows_client.service.saveEventResults(FileID)
        self._handle_messages(result)
        return result

    def downloadEventResults(self, EventCode):
        """Retrieve the latest imported results XML file (if any)
         for the given event.

        Params:
            EventCode: The event code of the event for which the results are
         retrieved.

        Return value: byte array containing the data of the XML file

        """
        result = self._ows_client.service.downloadEventResults(EventCode)
        self._handle_messages(result)
        return result

    def submitEventResults(self, EventCode):
        """Submit the events results to FEI for validation.After this operation,
         the results cannot be modified anymore.

        Params:
            EventCode: The event code of the event for which the results are
             submitted.

        Return value: True if the results have been correctly submitted.

        """
        result = self._ows_client.service.submitEventResults(EventCode)
        self._handle_messages(result)
        return result

    def getCompetitionsByEventCode(self, EventCode):
        """Retrieve a list of competitions by event code

        Params:
            EventCode: The code of the event you want the competitions from.

        Return value: An array of Competition objects

        """
        result = self._ows_client.service.getCompetitionsByEventCode(EventCode)
        self._handle_messages(result)
        return result.getCompetitionsByEventCodeResult

    def getCompetition(self, CompetitionCode):
        """Get a competition by its competition code

        Params:
            CompetitionCode: The code of the Competition you want to retrieve.

        Return value: A Competition object or None

        """
        result = self._ows_client.service.getCompetition(CompetitionCode)
        self._handle_messages(result)
        return result.getCompetitionResult

    def getCompetitions(self, CompetitionCodes):
        """Get a list competitions by their CompetitionCode

        Params:
            CompetitionCodes: An array of competitions codes.

        Return value: An array of Competition objects or None

        """
        string_array = self._ows_client.factory.create('ArrayOfString')
        string_array.string = CompetitionCodes
        result = self._ows_client.service.getCompetitions(string_array)
        self._handle_messages(result)
        return result.getCompetitionsResult

    def getCompetitionResults(self, CompetitionCode):
        """Retrieve a list of detailed results related to a competition given
         by its code.

        Params:
            CompetitionCode: The competition code you want to retrieve the
             results of.

        Return value: An array of NFResult objects.

        """
        result = self._ows_client.service.getCompetitionResults(CompetitionCode)
        self._handle_messages(result)
        return result.getCompetitionResultsResult

    def getPerson(self, PersonFEIID):
        """Get person based on FEI ID. It is also possible to get officials
         with this method.

        params:
            PersonFEIID: FEI ID of a FEI person.

        returns Person

        """
        result = self._ows_client.service.getPerson(PersonFEIID)
        self._handle_messages(result)
        return result.getPersonResult

    def getPersons(self, PersonFEIIDs):
        """Get a list of persons based on a list of FEI IDs

        params:
            PersonFEIIDs: A list of FEI IDs

        returns an array of Persons

        """
        int_array = self._ows_client.factory.create('ArrayOfInt')
        int_array.int = PersonFEIIDs
        result = self._ows_client.service.getPersons(int_array)
        self._handle_messages(result)
        return result.getPersonsResult

    def searchForPerson(self, Name=None, ID=None, Gender=None,
                        CompetingFor=None):
        """Search for persons in the FEI database.

        Params:
            Name: Name of the person you want to search for.
            ID: ID of the person you want to search for.
            Gender: Gender of the person you want to search for.
                Possible values: Male, Female
            CompetingFor: Country code of the person you want to search for.

        return Array of persons

        """
        sc = []
        factory = self._ows_client.factory
        if Name:
            criteria = factory.create('SCPersonAnyName')
            criteria.Name = Name
            criteria.Unconstrained = False
            sc.append(criteria)
        if ID:
            criteria = factory.create('SCPersonAnyID')
            criteria.ID = ID
            sc.append(criteria)
        if Gender:
            criteria = factory.create('SCPersonGender')
            criteria.Value = Gender
            sc.append(criteria)
        if CompetingFor:
            criteria = factory.create('SCPersonCompetingFor')
            criteria.Value = CompetingFor
            sc.append(criteria)
        if not sc:
            raise Exception('MissingConditions: You need to supply at least '
                            'one search criteria')

        sc_array = factory.create('ArrayOfSCBase')
        sc_array.SCBase = sc
        result = self._ows_client.service.searchForPerson(sc_array)
        self._handle_messages(result)
        return result.searchForPersonResult

    def getCompetitorHorses(self, PersonFEIID):
        """Returns a list of horses belonging to the rider with this FEI ID

        params:
            PersonFEIID: FEI ID of a rider.

        return  an array of Horses

        """
        result = self._ows_client.service.getCompetitorHorses(PersonFEIID)
        self._handle_messages(result)
        return result.getCompetitorHorsesResult

    def getCompetitorsHorses(self, PersonFEIIDs):
        """Returns a list of horses belonging to the riders with this FEI ID in
         the FEI IDs array

        params:
            PersonFEIIDs: An array of rider FEI IDs.

        return an array of Competitors

        """
        int_array = self._ows_client.factory.create('ArrayOfInt')
        int_array.int = PersonFEIIDs
        result = self._ows_client.service.getCompetitorsHorses(int_array)
        self._handle_messages(result)
        return result.getCompetitorsHorsesResult

    def getHorseColorList(self):
        """Retrieve a list of horse colors.

        Return value: an array of HorseColor objects

        """
        return self._ows_client.service.getHorseColorList()

    def getStudBookList(self):
        """Retrieve a list of known Stud Books

        Return value: an array of StudBook objects

        """
        return self._ows_client.service.getStudBookList()

    def searchForHorse(self, Name=None, ID=None, NameInclHistNames=None,
                       Pony=None, CurrentOwner=None, NF=None, Discipline=None):
        """Search for a horse matching the search criteria.

        Params:
            Name: Search horse by current name.
            ID: Search horse by any id field.
            NameInclHistNames: Search for horse by its current name and
             historical names.
            Pony: Search for pony(True/False).
            CurrentOwner: Search horse by its current owner.
            NF: Search horse by its registered national federation.
            Discipline: Search horse by its registered discipline.

        Return value: an array of zero or more Horse objects.

        """
        sc = []
        factory = self._ows_client.factory
        if Name:
            criteria = factory.create('SCHorseName')
            criteria.Name = Name
            sc.append(criteria)
        if ID:
            criteria = factory.create('SCHorseAnyID')
            criteria.ID = ID
            sc.append(criteria)
        if NameInclHistNames:
            criteria = factory.create('SCHorseInclHistNames')
            criteria.Value = NameInclHistNames
            sc.append(criteria)
        if Pony:
            criteria = factory.create('SCHorsePony')
            criteria.Value = Pony
            sc.append(criteria)
        if CurrentOwner:
            criteria = factory.create('SCHorseCurrentOwner')
            criteria.Value = CurrentOwner
            sc.append(criteria)
        if NF:
            criteria = factory.create('SCHorseAdminNF')
            criteria.Value = NF
            sc.append(criteria)
        if Discipline:
            criteria = factory.create('SCHorseRegDiscipline')
            criteria.Value = Discipline
            sc.append(criteria)
        sc_array = factory.create('ArrayOfSCBase')
        sc_array.SCBase = sc
        result = self._ows_client.service.searchForHorse(sc_array)
        self._handle_messages(result)
        return result.searchForHorseResult

    def getHorse(self, HorseFEICode):
        """Retrieve a horse by FEI code.

        Params:
            HorseFEICode: The FEI code of the horse to retrieve.

        Return value: A Horse object or None.

        """
        result = self._ows_client.service.getHorse(HorseFEICode)
        self._handle_messages(result)
        return result.getHorseResult

    def getHorses(self, HorseFEICodes):
        """Retrieve a list of horses by FEI code.

        Params:
            HorseFEICodes: The FEI codes of the horses to retrieve.

        Return value: An array of Horse objects.

        """
        string_array = self._ows_client.factory.create('ArrayOfString')
        string_array.string = HorseFEICodes
        result = self._ows_client.service.getHorses(string_array)
        self._handle_messages(result)
        return result.getHorsesResult

    def getHorseOwner(self, HorseFEICode):
        """Retrieve the current horse owner.

        Params:
            HorseFEICode: The FEI code of the horse, which owner to retrieve.

        Return value: a HorseOwner object

        """
        result = self._ows_client.service.getHorseOwner(HorseFEICode)
        self._handle_messages(result)
        return result.getHorseOwnerResult

    def getHorseCompetitors(self, HorseFEICode):
        """Retrieve the competitors associated to the horse

        Params:
            HorseFEICode: The FEI code of the horse

        Return value: a list of competitors associated with this horse.

        """
        result = self._ows_client.service.getHorseCompetitors(HorseFEICode)
        self._handle_messages(result)
        return result.getHorseCompetitorsResult

    def getHorsesCompetitors(self, HorseFEICodes):
        """Retrieve the competitors associated to the horses

        Params:
            HorseFEICodes: An array of FEI codes belonging to horses

        Return value: A list of horses with competitors

        """
        string_array = self._ows_client.factory.create('ArrayOfString')
        string_array.string = HorseFEICodes
        result = self._ows_client.service.getHorsesCompetitors(string_array)
        self._handle_messages(result)
        return result.getHorsesCompetitorsResult
