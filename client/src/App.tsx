import { useEffect, useMemo, useState } from 'react';
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from './components/ui/table';
import { Button } from './components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from './components/ui/dialog';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from './components/ui/card';
import { Input } from './components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from './components/ui/select';
import { ArrowUpDown } from 'lucide-react';

interface Candidate {
  0: number; // id
  1: {
    candidate: {
      fullName: string;
      primaryProfession: string;
    };
    skills: { name: string }[];
  };
}

function App() {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [jobs, setJobs] = useState<string[]>([]);
  const [jobFilter, setJobFilter] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [sortConfig, setSortConfig] = useState<{ key: keyof Candidate[1]['candidate'] | 'skills'; direction: 'ascending' | 'descending' } | null>(null);

  useEffect(() => {
    fetch('/api/candidates')
      .then((res) => res.json())
      .then((data) => {
        setCandidates(data);
      });

    fetch('/api/jobs')
      .then((res) => res.json())
      .then((data) => setJobs(data));
  }, []);

  const filteredCandidates = useMemo(() => {
    let filtered = candidates;

    if (jobFilter) {
      filtered = filtered.filter(
        (candidate) => candidate[1].candidate.primaryProfession === jobFilter
      );
    }

    if (searchQuery) {
      filtered = filtered.filter((candidate) =>
        Object.values(candidate[1].candidate).some((value) =>
          String(value).toLowerCase().includes(searchQuery.toLowerCase())
        ) ||
        candidate[1].skills.some((skill) =>
          skill.name.toLowerCase().includes(searchQuery.toLowerCase())
        )
      );
    }

    if (sortConfig !== null) {
      filtered.sort((a, b) => {
        let aValue: string | number;
        let bValue: string | number;

        if (sortConfig.key === 'skills') {
          aValue = a[1].skills.map((s) => s.name).join(', ');
          bValue = b[1].skills.map((s) => s.name).join(', ');
        } else {
          aValue = a[1].candidate[sortConfig.key];
          bValue = b[1].candidate[sortConfig.key];
        }

        if (aValue < bValue) {
          return sortConfig.direction === 'ascending' ? -1 : 1;
        }
        if (aValue > bValue) {
          return sortConfig.direction === 'ascending' ? 1 : -1;
        }
        return 0;
      });
    }

    return filtered;
  }, [jobFilter, searchQuery, candidates, sortConfig]);

  const requestSort = (key: keyof Candidate[1]['candidate'] | 'skills') => {
    let direction: 'ascending' | 'descending' = 'ascending';
    if (sortConfig && sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  const clearFilters = () => {
    setJobFilter('');
    setSearchQuery('');
    setSortConfig(null);
  };

  return (
    <div className="container mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle>Candidate Management</CardTitle>
          <CardDescription>Search and filter candidates.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex space-x-4 mb-4">
            <Select onValueChange={(value) => setJobFilter(value === 'all' ? '' : value)} value={jobFilter}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Filter by Job" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Jobs</SelectItem>
                {jobs.map((job) => (
                  <SelectItem key={job} value={job}>
                    {job}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Input
              placeholder="Global Search"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="max-w-sm"
            />
            <Button onClick={clearFilters} variant="outline">
              Clear Filters
            </Button>
          </div>
          <Table>
            <TableHeader>
              <TableRow className="bg-muted/50 border-b border-gold-darker">
                <TableHead className="w-1/4 cursor-pointer" onClick={() => requestSort('fullName')}>
                  <div className="flex items-center">
                    Name <ArrowUpDown className="ml-2 h-4 w-4" />
                  </div>
                </TableHead>
                <TableHead className="w-1/4 cursor-pointer" onClick={() => requestSort('primaryProfession')}>
                  <div className="flex items-center">
                    Job <ArrowUpDown className="ml-2 h-4 w-4" />
                  </div>
                </TableHead>
                <TableHead className="cursor-pointer" onClick={() => requestSort('skills')}>
                  <div className="flex items-center">
                    Skills <ArrowUpDown className="ml-2 h-4 w-4" />
                  </div>
                </TableHead>
                <TableHead className="w-24">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredCandidates.map((candidate) => (
                <TableRow key={candidate[0]}>
                  <TableCell>{candidate[1].candidate.fullName}</TableCell>
                  <TableCell>
                    {candidate[1].candidate.primaryProfession}
                  </TableCell>
                  <TableCell>
                    {candidate[1].skills.map((skill) => skill.name).join(', ')}
                  </TableCell>
                  <TableCell>
                    <Dialog>
                      <DialogTrigger asChild>
                        <Button>View</Button>
                      </DialogTrigger>
                      <DialogContent className="sm:max-w-[800px]">
                        <DialogHeader>
                          <DialogTitle>
                            {candidate[1].candidate.fullName}
                          </DialogTitle>
                        </DialogHeader>
                        <iframe
                          src={`/candidate/${candidate[0]}`}
                          style={{
                            width: '100%',
                            height: '80vh',
                            border: 'none',
                          }}
                        />
                      </DialogContent>
                    </Dialog>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}

export default App;
