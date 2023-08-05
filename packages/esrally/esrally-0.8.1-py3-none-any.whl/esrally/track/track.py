import logging
from enum import Enum

logger = logging.getLogger("rally.track")


class Index:
    """
    Defines an index in Elasticsearch.
    """

    def __init__(self, name, auto_managed, types):
        """

        Creates a new index.

        :param name: The index name. Mandatory.
        :param auto_managed: True iff Rally should automatically manage this index (i.e. it can create and delete it at will).
        :param types: A list of types. Should contain at least one type.
        """
        self.name = name
        self.auto_managed = auto_managed
        self.types = types

    def matches(self, pattern):
        if pattern is None:
            return True
        elif pattern in ["_all", "*"]:
            return True
        elif self.name == pattern:
            return True
        else:
            return False

    @property
    def number_of_documents(self):
        num_docs = 0
        for t in self.types:
            num_docs += t.number_of_documents
        return num_docs

    @property
    def compressed_size_in_bytes(self):
        size = 0
        for t in self.types:
            if t.compressed_size_in_bytes is not None:
                size += t.compressed_size_in_bytes
            else:
                return None
        return size

    @property
    def uncompressed_size_in_bytes(self):
        size = 0
        for t in self.types:
            if t.uncompressed_size_in_bytes is not None:
                size += t.uncompressed_size_in_bytes
            else:
                return None
        return size

    def __str__(self):
        return self.name

    def __repr__(self):
        r = []
        for prop, value in vars(self).items():
            r.append("%s = [%s]" % (prop, repr(value)))
        return ", ".join(r)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


class IndexTemplate:
    """
    Defines an index template in Elasticsearch.
    """

    def __init__(self, name, pattern, content, delete_matching_indices):
        """

        Creates a new index template.

        :param name: Name of the index template. Mandatory.
        :param pattern: The index pattern to which the index template applies. Mandatory.
        :param content: The content of the corresponding template. Mandatory.
        :param delete_matching_indices: Delete all indices that match the pattern before the benchmark iff True.
        """
        self.name = name
        self.pattern = pattern
        self.content = content
        self.delete_matching_indices = delete_matching_indices

    def __str__(self, *args, **kwargs):
        return self.name

    def __repr__(self):
        r = []
        for prop, value in vars(self).items():
            r.append("%s = [%s]" % (prop, repr(value)))
        return ", ".join(r)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


class Type:
    """
    Defines a type in Elasticsearch.
    """

    def __init__(self, name, mapping, document_file=None, document_archive=None, includes_action_and_meta_data=False,
                 number_of_documents=0, compressed_size_in_bytes=0, uncompressed_size_in_bytes=0):
        """

        Creates a new type. Mappings are mandatory but the document_archive (and associated properties) are optional.

        :param name: The name of this type. Mandatory.
        :param mapping: The type's mapping. Mandatory.
        :param document_file: The file name of benchmark documents after decompression. Optional (e.g. for percolation we
        just need a mapping but no documents)
        :param document_archive: The file name of the compressed benchmark document name on the remote server. Optional (e.g. for
        percolation we just need a mapping but no documents)
        :param includes_action_and_meta_data: True, if the source file already includes the action and meta-data line. False, if it only
        contains documents.
        :param number_of_documents: The number of documents in the benchmark document. Needed for proper progress reporting. Only needed if
         a document_archive is given.
        :param compressed_size_in_bytes: The compressed size in bytes of the benchmark document. Needed for verification of the download and
         user reporting. Only useful if a document_archive is given (optional but recommended to be set).
        :param uncompressed_size_in_bytes: The size in bytes of the benchmark document after decompressing it. Only useful if a
        document_archive is given (optional but recommended to be set).
        """
        self.name = name
        self.mapping = mapping
        self.document_file = document_file
        self.document_archive = document_archive
        self.includes_action_and_meta_data = includes_action_and_meta_data
        self.number_of_documents = number_of_documents
        self.compressed_size_in_bytes = compressed_size_in_bytes
        self.uncompressed_size_in_bytes = uncompressed_size_in_bytes

    def has_valid_document_data(self):
        return (self.has_compressed_corpus() or self.has_uncompressed_corpus()) and self.number_of_documents > 0

    def has_compressed_corpus(self):
        return self.document_archive is not None

    def has_uncompressed_corpus(self):
        return self.document_file is not None

    @property
    def number_of_lines(self):
        if self.includes_action_and_meta_data:
            return self.number_of_documents * 2
        else:
            return self.number_of_documents

    def __str__(self, *args, **kwargs):
        return self.name

    def __repr__(self):
        r = []
        for prop, value in vars(self).items():
            r.append("%s = [%s]" % (prop, repr(value)))
        return ", ".join(r)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


class Track:
    """
    A track defines the data set that is used. It corresponds loosely to a use case (e.g. logging, event processing, analytics, ...)
    """

    def __init__(self, name, description, source_root_url=None, meta_data=None, challenges=None, indices=None,
                 templates=None, has_plugins=False):
        """

        Creates a new track.

        :param name: A short, descriptive name for this track. As per convention, this name should be in lower-case without spaces.
        :param description: A description for this track (should be less than 80 characters).
        :param source_root_url: The publicly reachable http URL of the root folder for this track (without a trailing slash). Directly
        below this URL the benchmark document files have to be located.
        :param meta_data: An optional dict of meta-data elements to attach to each metrics record. Default: {}.
        :param challenges: A list of one or more challenges to use. Precondition: If the list is non-empty it contains exactly one element
        with its ``default`` property set to ``True``.
        :param indices: A list of indices for this track. May be None. One of `indices` or `templates` must be set though.
        :param templates: A list of index templates for this track. May be None. One of `indices` or `templates` must be set though.
        :param has_plugins: True iff the track also defines plugins (e.g. custom runners or parameter sources).
        """
        self.name = name
        self.meta_data = meta_data if meta_data else {}
        self.description = description
        self.source_root_url = source_root_url
        self.challenges = challenges if challenges else []
        self.indices = indices if indices else []
        self.templates = templates if templates else []
        self.has_plugins = has_plugins

    @property
    def default_challenge(self):
        for challenge in self.challenges:
            if challenge.default:
                return challenge
        # This should only happen if we don't have any challenges
        return None

    def find_challenge_or_default(self, name):
        """
        :param name: The name of the challenge to find.
        :return: The challenge with the given name. The default challenge, if the name is "" or ``None``. Otherwise, returns ``None``.
        """
        if name in [None, ""]:
            return self.default_challenge
        for challenge in self.challenges:
            if challenge.name == name:
                return challenge
        return None

    @property
    def number_of_documents(self):
        num_docs = 0
        if self.indices:
            for index in self.indices:
                num_docs += index.number_of_documents
        return num_docs

    @property
    def compressed_size_in_bytes(self):
        size = 0
        if self.indices:
            for index in self.indices:
                if index.compressed_size_in_bytes is not None:
                    size += index.compressed_size_in_bytes
                else:
                    return None
        return size

    @property
    def uncompressed_size_in_bytes(self):
        size = 0
        if self.indices:
            for index in self.indices:
                if index.uncompressed_size_in_bytes is not None:
                    size += index.uncompressed_size_in_bytes
                else:
                    return None
        return size

    def __str__(self):
        return self.name

    def __repr__(self):
        r = []
        for prop, value in vars(self).items():
            r.append("%s = [%s]" % (prop, repr(value)))
        return ", ".join(r)

    def __hash__(self):
        return hash(self.name) ^ hash(self.meta_data) ^ hash(self.description) ^ hash(self.source_root_url) ^ hash(self.challenges) ^ \
               hash(self.indices) ^ hash(self.templates)

    def __eq__(self, othr):
        return (isinstance(othr, type(self)) and
                (self.name, self.meta_data, self.description, self.source_root_url, self.challenges, self.indices, self.templates) ==
                (othr.name, othr.meta_data, othr.description, othr.source_root_url, othr.challenges, othr.indices, othr.templates))


class Challenge:
    """
    A challenge defines the concrete operations that will be done.
    """

    def __init__(self,
                 name,
                 description=None,
                 user_info=None,
                 index_settings=None,
                 cluster_settings=None,
                 default=False,
                 meta_data=None,
                 schedule=None):
        self.name = name
        self.meta_data = meta_data if meta_data else {}
        self.description = description
        self.user_info = user_info
        self.index_settings = index_settings if index_settings else {}
        self.cluster_settings = cluster_settings if cluster_settings else {}
        self.default = default
        self.schedule = schedule if schedule else []

    def remove_task(self, task):
        self.schedule.remove(task)

    def __str__(self):
        return self.name

    def __repr__(self):
        r = []
        for prop, value in vars(self).items():
            r.append("%s = [%s]" % (prop, repr(value)))
        return ", ".join(r)

    def __hash__(self):
        return hash(self.name) ^ hash(self.description) ^ hash(self.index_settings) ^ hash(self.cluster_settings) ^ hash(self.default) ^ \
               hash(self.meta_data) ^ hash(self.schedule)

    def __eq__(self, othr):
        return (isinstance(othr, type(self)) and
                (self.name, self.description, self.index_settings, self.cluster_settings, self.default, self.meta_data, self.schedule) ==
                (othr.name, othr.description, othr.index_settings, othr.cluster_settings, othr.default, othr.meta_data, othr.schedule))


class OperationType(Enum):
    Index = 0,
    ForceMerge = 1,
    IndicesStats = 2,
    NodesStats = 3,
    Search = 4,
    ClusterHealth = 5,
    Bulk = 6,
    PutPipeline = 7,
    Refresh = 8

    @classmethod
    def from_hyphenated_string(cls, v):
        if v == "index":
            return OperationType.Index
        elif v == "force-merge":
            return OperationType.ForceMerge
        elif v == "index-stats":
            return OperationType.IndicesStats
        elif v == "node-stats":
            return OperationType.NodesStats
        elif v == "search":
            return OperationType.Search
        elif v == "cluster-health":
            return OperationType.ClusterHealth
        elif v == "bulk":
            return OperationType.Bulk
        elif v == "put-pipeline":
            return OperationType.PutPipeline
        elif v == "refresh":
            return OperationType.Refresh
        else:
            raise KeyError("No enum value for [%s]" % v)


class TaskNameFilter:
    def __init__(self, name):
        self.name = name

    def matches(self, task):
        return self.name == task.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.name == other.name

    def __str__(self, *args, **kwargs):
        return "filter for task name [%s]" % self.name


class TaskOpTypeFilter:
    def __init__(self, op_type_name):
        # we need to use the string representation because users may define their own operation types via a custom runners.
        try:
            self.op_type = OperationType.from_hyphenated_string(op_type_name).name
        except KeyError:
            self.op_type = op_type_name

    def matches(self, task):
        return self.op_type == task.operation.type

    def __hash__(self):
        return hash(self.op_type)

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.op_type == other.op_type

    def __str__(self, *args, **kwargs):
        return "filter for operation type [%s]" % self.op_type


# Schedule elements
class Parallel:
    def __init__(self, tasks, clients=None):
        self.tasks = tasks
        self._clients = clients

    @property
    def clients(self):
        if self._clients is not None:
            return self._clients
        else:
            num_clients = 0
            for task in self.tasks:
                num_clients += task.clients
            return num_clients

    def matches(self, task_filter):
        # a parallel element matches if any of its elements match
        for task in self.tasks:
            if task.matches(task_filter):
                return True
        return False

    def remove_task(self, task):
        self.tasks.remove(task)

    def __iter__(self):
        return iter(self.tasks)

    def __str__(self, *args, **kwargs):
        return "%d parallel tasks" % len(self.tasks)

    def __repr__(self):
        r = []
        for prop, value in vars(self).items():
            r.append("%s = [%s]" % (prop, repr(value)))
        return ", ".join(r)

    def __hash__(self):
        return hash(self.tasks)

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.tasks == other.tasks


class Task:
    def __init__(self, name, operation, meta_data=None, warmup_iterations=0, iterations=1, warmup_time_period=None, time_period=None, clients=1,
                 completes_parent=False, schedule="deterministic", params=None):
        self.name = name
        self.operation = operation
        self.meta_data = meta_data if meta_data else {}
        self.warmup_iterations = warmup_iterations
        self.iterations = iterations
        self.warmup_time_period = warmup_time_period
        self.time_period = time_period
        self.clients = clients
        self.completes_parent = completes_parent
        self.schedule = schedule
        self.params = params if params else {}

    def matches(self, task_filter):
        return task_filter.matches(self)

    def __hash__(self):
        # Note that we do not include `params` in __hash__ and __eq__ (the other attributes suffice to uniquely define a task)
        return hash(self.name) ^ hash(self.operation) ^ hash(self.warmup_iterations) ^ hash(self.iterations) ^ \
               hash(self.warmup_time_period) ^ hash(self.time_period) ^ hash(self.clients) ^ hash(self.schedule) ^ \
               hash(self.completes_parent)

    def __eq__(self, other):
        # Note that we do not include `params` in __hash__ and __eq__ (the other attributes suffice to uniquely define a task)
        return isinstance(other, type(self)) and (self.name, self.operation, self.warmup_iterations, self.iterations,
                                                  self.warmup_time_period, self.time_period, self.clients, self.schedule,
                                                  self.completes_parent) == (other.name, other.operation, other.warmup_iterations,
                                                                             other.iterations, other.warmup_time_period, other.time_period,
                                                                             other.clients, other.schedule, other.completes_parent)

    def __iter__(self):
        return iter([self])

    def __str__(self, *args, **kwargs):
        return self.name

    def __repr__(self):
        r = []
        for prop, value in vars(self).items():
            r.append("%s = [%s]" % (prop, repr(value)))
        return ", ".join(r)


class Operation:
    def __init__(self, name, operation_type, meta_data=None, params=None, param_source=None):
        if params is None:
            params = {}
        self.name = name
        self.meta_data = meta_data if meta_data else {}
        self.type = operation_type
        self.params = params
        self.param_source = param_source

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.name == other.name

    def __str__(self, *args, **kwargs):
        return self.name

    def __repr__(self):
        r = []
        for prop, value in vars(self).items():
            r.append("%s = [%s]" % (prop, repr(value)))
        return ", ".join(r)
