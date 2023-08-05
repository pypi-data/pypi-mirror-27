import csv
from builtins import super

from phigaro.data import read_genemark_output, read_hmmer_output, hmmer_res_to_npn, Gene
from phigaro.finder.v2 import V2Finder
from .base import AbstractTask
from .gene_mark import GeneMarkTask
from .hmmer import HmmerTask


class RunPhigaroTask(AbstractTask):
    task_name = 'run_phigaro'

    def __init__(self, hmmer_task, gene_mark_task):
        """
        :type hmmer_task: HmmerTask
        :type gene_mark_task: GeneMarkTask
        """
        super().__init__()
        self.hmmer_task = hmmer_task
        self.gene_mark_task = gene_mark_task

    def _prepare(self):
        self.finder = V2Finder(
            window_len=self.config['phigaro']['window_len'],
            threshold_min=self.config['phigaro']['threshold_min'],
            threshold_max=self.config['phigaro']['threshold_max'],
        )
        self._print_vogs = self.config['phigaro'].get('print_vogs', False)

    def output(self):
        return self.file('{}.tsv'.format(self.sample))

    def run(self):
        max_evalue = self.config['hmmer']['e_value_threshold']

        scaffold_set = read_genemark_output(self.gene_mark_task.output())
        hmmer_result = read_hmmer_output(self.hmmer_task.output())

        with open(self.output(), 'w') as of:
            writer = csv.writer(of, delimiter='\t')

            if self._print_vogs:
                writer.writerow(('scaffold', 'begin', 'end', 'vog'))
            else:
                writer.writerow(('scaffold', 'begin', 'end'))

            for scaffold in scaffold_set:
                genes = list(scaffold)  # type: list[Gene]
                npn = hmmer_res_to_npn(scaffold, hmmer_result, max_evalue=max_evalue)

                phages = self.finder.find_phages(npn)
                for phage in phages:
                    begin = genes[phage.begin].begin
                    end = genes[phage.end].end
                    if self._print_vogs:
                        hmmer_records = (
                            hmmer_result.min_record(hmmer_result.get_records(scaffold.name, gene.name))
                            for gene in genes[phage.begin: phage.end]
                        )

                        hmmer_records = (
                            record.vog_name
                            for record in hmmer_records
                            if record and record.evalue <= max_evalue
                        )

                        hmmer_records_str = ','.join(hmmer_records)
                        writer.writerow((scaffold.name, begin, end, hmmer_records_str))
                    else:
                        writer.writerow((scaffold.name, begin, end))

