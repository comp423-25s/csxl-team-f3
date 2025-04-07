import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
  CircularProgress,
} from '@mui/material';
import { useParams } from 'react-router-dom';
import { StudyGuide, PracticeProblem, StudentProgress } from '../types/studyBuddy';

const StudyBuddyPage: React.FC = () => {
  const { courseId } = useParams<{ courseId: string }>();
  const [topics, setTopics] = useState<string[]>([]);
  const [selectedTopics, setSelectedTopics] = useState<string[]>([]);
  const [studyGuide, setStudyGuide] = useState<StudyGuide | null>(null);
  const [practiceProblems, setPracticeProblems] = useState<PracticeProblem[]>([]);
  const [progress, setProgress] = useState<StudentProgress[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Fetch available topics for the course
    fetchTopics();
    // Fetch student's progress
    fetchProgress();
  }, [courseId]);

  const fetchTopics = async () => {
    try {
      const response = await fetch(`/api/study-buddy/courses/${courseId}/topics`);
      const data = await response.json();
      setTopics(data);
    } catch (error) {
      console.error('Error fetching topics:', error);
    }
  };

  const fetchProgress = async () => {
    try {
      const response = await fetch(`/api/study-buddy/progress/${courseId}`);
      const data = await response.json();
      setProgress(data);
    } catch (error) {
      console.error('Error fetching progress:', error);
    }
  };

  const generateStudyGuide = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/study-buddy/study-guides', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          course_id: courseId,
          topics: selectedTopics,
        }),
      });
      const data = await response.json();
      setStudyGuide(data);
    } catch (error) {
      console.error('Error generating study guide:', error);
    }
    setLoading(false);
  };

  const startPracticeSession = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/study-buddy/study-sessions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          course_id: courseId,
          topics: selectedTopics,
        }),
      });
      const data = await response.json();
      setPracticeProblems(data.problems);
    } catch (error) {
      console.error('Error starting practice session:', error);
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Rameses Study Buddy
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Select Topics
                </Typography>
                <FormControl fullWidth>
                  <InputLabel>Topics</InputLabel>
                  <Select
                    multiple
                    value={selectedTopics}
                    onChange={(e) => setSelectedTopics(e.target.value as string[])}
                    renderValue={(selected) => (
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {selected.map((value) => (
                          <Chip key={value} label={value} />
                        ))}
                      </Box>
                    )}
                  >
                    {topics.map((topic) => (
                      <MenuItem key={topic} value={topic}>
                        {topic}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
                  <Button
                    variant="contained"
                    onClick={generateStudyGuide}
                    disabled={loading || selectedTopics.length === 0}
                  >
                    Generate Study Guide
                  </Button>
                  <Button
                    variant="outlined"
                    onClick={startPracticeSession}
                    disabled={loading || selectedTopics.length === 0}
                  >
                    Start Practice Session
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={8}>
            {loading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
                <CircularProgress />
              </Box>
            ) : studyGuide ? (
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Study Guide
                  </Typography>
                  <div dangerouslySetInnerHTML={{ __html: studyGuide.content }} />
                </CardContent>
              </Card>
            ) : practiceProblems.length > 0 ? (
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Practice Problems
                  </Typography>
                  {practiceProblems.map((problem, index) => (
                    <Box key={problem.id} sx={{ mb: 3 }}>
                      <Typography variant="subtitle1">
                        Question {index + 1}
                      </Typography>
                      <Typography>{problem.question_text}</Typography>
                      {/* Add answer input and submission logic here */}
                    </Box>
                  ))}
                </CardContent>
              </Card>
            ) : null}
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default StudyBuddyPage; 